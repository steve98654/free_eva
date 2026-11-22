// Cloudflare Worker for evaxie.us.
//
// Serves the static Astro build (env.ASSETS) and a small petition API:
//   GET  /api/petition          -> signature count + public signer list (names/cities only)
//   POST /api/petition/sign     -> record a signature, send a confirmation email
//   POST /api/petition/remove   -> delete a signature using the token from the email
//   GET  /api/petition/export   -> all signers for the Google Sheet sync (needs EXPORT_TOKEN)
//
// Bindings and settings (see wrangler.jsonc and site/PETITION.md):
//   DB                    D1 database (required for signing)
//   SITE_URL              e.g. https://evaxie.us
//   EMAIL_FROM            e.g. "Free Eva <petition@evaxie.us>" (must be a verified Resend domain)
//   EMAIL_REPLY_TO        e.g. weare@geodesic.pro
//   TURNSTILE_SITE_KEY    public Turnstile key (optional; spam check is skipped if unset)
//   TURNSTILE_SECRET_KEY  secret  (wrangler secret / dashboard "Secret")
//   RESEND_API_KEY        secret  (if unset, signatures still save but no email is sent)
//   IP_SALT               secret  (optional; salts the IP hash used for rate limiting)
//   EXPORT_TOKEN          secret  (shared with the Google Sheet script; export is off if unset)

interface Env {
  ASSETS: { fetch: (req: Request) => Promise<Response> };
  DB?: D1Database;
  SITE_URL?: string;
  EMAIL_FROM?: string;
  EMAIL_REPLY_TO?: string;
  TURNSTILE_SITE_KEY?: string;
  TURNSTILE_SECRET_KEY?: string;
  RESEND_API_KEY?: string;
  IP_SALT?: string;
  EXPORT_TOKEN?: string;
}

// Minimal D1 types so this file needs no extra dev dependency.
interface D1Result<T = unknown> { results: T[]; meta?: { changes?: number } }
interface D1PreparedStatement {
  bind(...values: unknown[]): D1PreparedStatement;
  first<T = unknown>(): Promise<T | null>;
  all<T = unknown>(): Promise<D1Result<T>>;
  run(): Promise<D1Result>;
}
interface D1Database {
  prepare(query: string): D1PreparedStatement;
  batch(statements: D1PreparedStatement[]): Promise<D1Result[]>;
}
interface ExecutionContext { waitUntil(p: Promise<unknown>): void }

const PAGE_SIZE = 50;
const MAX_PER_IP_PER_HOUR = 5;

const AFFILIATIONS: Record<string, string> = {
  student: 'Princeton student',
  faculty_staff: 'Princeton faculty or staff',
  alum: 'Princeton alum',
  community: 'Community member',
};
const HEARD_FROM: Record<string, string> = {
  qr: 'QR code (shirt, poster, sticker)',
  social: 'Social media',
  rally: 'Rally or event',
  friend: 'Friend or colleague',
  news: 'News story',
  email: 'Email or group chat',
  other: 'Other',
};

// ---------- schema ----------
// The Worker keeps the D1 schema current itself, so no manual SQL is needed after deploys.
// Mirrors migrations/0001 and 0002.

const COLUMNS = `
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  city TEXT, state TEXT, zip TEXT, affiliation TEXT, comment TEXT, heard_from TEXT,
  is_public INTEGER NOT NULL DEFAULT 0,
  wants_updates INTEGER NOT NULL DEFAULT 0,
  signed_at TEXT NOT NULL,
  manage_token TEXT NOT NULL UNIQUE,
  ip_hash TEXT, email_sent_at TEXT, email_error TEXT`;
const OLD_COLS = 'id, name, email, city, is_public, wants_updates, signed_at, manage_token, ip_hash, email_sent_at, email_error';
let schemaReady = false;

async function ensureSchema(db: D1Database): Promise<void> {
  if (schemaReady) return;
  const info = await db.prepare('PRAGMA table_info(signatures)').all<{ name: string; notnull: number }>();
  const cols = info.results;
  const indexes = [
    db.prepare('CREATE INDEX IF NOT EXISTS idx_signatures_public ON signatures (is_public, signed_at DESC)'),
    db.prepare('CREATE INDEX IF NOT EXISTS idx_signatures_ip ON signatures (ip_hash, signed_at)'),
  ];
  if (cols.length === 0) {
    await db.batch([db.prepare(`CREATE TABLE IF NOT EXISTS signatures (${COLUMNS})`), ...indexes]);
  } else if (!cols.some((c) => c.name === 'affiliation')) {
    // 0002: email becomes optional (needs a table rebuild in SQLite) and new optional fields.
    await db.batch([
      db.prepare('DROP TABLE IF EXISTS signatures_v2'),
      db.prepare(`CREATE TABLE signatures_v2 (${COLUMNS})`),
      db.prepare(`INSERT INTO signatures_v2 (${OLD_COLS}) SELECT ${OLD_COLS} FROM signatures`),
      db.prepare('DROP TABLE signatures'),
      db.prepare('ALTER TABLE signatures_v2 RENAME TO signatures'),
      ...indexes,
    ]);
  }
  schemaReady = true;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    if (!url.pathname.startsWith('/api/')) return env.ASSETS.fetch(request);

    try {
      if (env.DB) await ensureSchema(env.DB);
      if (url.pathname === '/api/petition/export' && request.method === 'GET') return await exportAll(request, env);
      if (url.pathname === '/api/petition' && request.method === 'GET') return await getPetition(url, env);
      if (url.pathname === '/api/petition/sign' && request.method === 'POST') return await sign(request, env, ctx);
      if (url.pathname === '/api/petition/remove' && request.method === 'POST') return await remove(request, env);
      return json({ error: 'Not found' }, 404);
    } catch (err) {
      console.error('petition api error', err);
      return json({ error: 'Something went wrong on our side. Please try again in a minute.' }, 500);
    }
  },
};

// ---------- GET /api/petition ----------

async function getPetition(url: URL, env: Env): Promise<Response> {
  const base = { turnstileSiteKey: env.TURNSTILE_SITE_KEY || null };
  if (!env.DB) return json({ ...base, ready: false, count: 0, signers: [], nextCursor: null });

  const cursor = Number(url.searchParams.get('cursor')) || 0;
  const countRow = await env.DB.prepare('SELECT COUNT(*) AS n FROM signatures').first<{ n: number }>();
  const rows = await env.DB.prepare(
    `SELECT id, name, city, state, signed_at FROM signatures
     WHERE is_public = 1 ${cursor ? 'AND id < ?1' : ''}
     ORDER BY id DESC LIMIT ${PAGE_SIZE + 1}`,
  )
    .bind(...(cursor ? [cursor] : []))
    .all<{ id: number; name: string; city: string | null; state: string | null; signed_at: string }>();

  const list = rows.results.slice(0, PAGE_SIZE);
  return json(
    {
      ...base,
      ready: true,
      count: countRow?.n ?? 0,
      // Only public signers, and only name, city and time. Never email.
      signers: list.map((r) => ({ name: r.name, city: r.city, state: r.state, signedAt: r.signed_at })),
      nextCursor: rows.results.length > PAGE_SIZE ? list[list.length - 1].id : null,
    },
    200,
    { 'cache-control': 'public, max-age=15' },
  );
}

// ---------- POST /api/petition/sign ----------

async function sign(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
  if (!env.DB) return json({ error: 'Online signing opens soon. Please check back shortly.' }, 503);

  const body = await readBody(request);
  if (!body) return json({ error: 'Could not read the form. Please try again.' }, 400);

  // Honeypot: real people never fill this hidden field.
  if (clean(body.website, 200)) return json({ ok: true, signedAt: new Date().toISOString() });

  const name = clean(body.name, 80);
  const email = clean(body.email, 254).toLowerCase();
  const city = clean(body.city, 80) || null;
  const state = clean(body.state, 40) || null;
  const zip = clean(body.zip, 12) || null;
  const affiliation = AFFILIATIONS[clean(body.affiliation, 20)] ? clean(body.affiliation, 20) : null;
  const heardFrom = HEARD_FROM[clean(body.heardFrom, 20)] ? clean(body.heardFrom, 20) : null;
  const comment = cleanMultiline(body.comment, 500) || null;
  const isPublic = truthy(body.public);
  const wantsUpdates = truthy(body.updates);

  if (name.length < 2) return json({ error: 'Please enter your name.', field: 'name' }, 400);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return json({ error: 'Please enter a valid email address.', field: 'email' }, 400);
  if (!truthy(body.agree)) return json({ error: 'Please tick the box to confirm you agree with the petition.', field: 'agree' }, 400);

  const ip = request.headers.get('cf-connecting-ip') || '';
  if (env.TURNSTILE_SECRET_KEY) {
    const ok = await verifyTurnstile(env.TURNSTILE_SECRET_KEY, String(body.turnstileToken || ''), ip);
    if (!ok) return json({ error: 'We could not confirm you are human. Please reload the page and try again.' }, 400);
  }

  const ipHash = ip ? await sha256(`${env.IP_SALT || 'evaxie'}:${ip}`) : null;
  if (ipHash) {
    const since = new Date(Date.now() - 3600_000).toISOString();
    const recent = await env.DB.prepare('SELECT COUNT(*) AS n FROM signatures WHERE ip_hash = ?1 AND signed_at > ?2')
      .bind(ipHash, since)
      .first<{ n: number }>();
    if ((recent?.n ?? 0) >= MAX_PER_IP_PER_HOUR) {
      return json({ error: 'Too many signatures from this network in the last hour. Please try again later.' }, 429);
    }
  }

  const existing = email ? await env.DB.prepare('SELECT id FROM signatures WHERE email = ?1').bind(email).first() : null;
  if (existing) return json({ error: 'This email address has already signed. Thank you!', field: 'email', duplicate: true }, 409);
  if (!email && ipHash) {
    // Without an email we can't dedupe exactly; block the same name signing twice from the same network.
    const same = await env.DB.prepare('SELECT id FROM signatures WHERE lower(name) = lower(?1) AND ip_hash = ?2')
      .bind(name, ipHash)
      .first();
    if (same) return json({ error: 'It looks like you have already signed. Thank you!', field: 'name', duplicate: true }, 409);
  }

  const signedAt = new Date().toISOString();
  const token = randomToken();
  await env.DB.prepare(
    `INSERT INTO signatures (name, email, city, state, zip, affiliation, comment, heard_from,
                             is_public, wants_updates, signed_at, manage_token, ip_hash)
     VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13)`,
  )
    .bind(name, email || null, city, state, zip, affiliation, comment, heardFrom,
      isPublic ? 1 : 0, wantsUpdates && email ? 1 : 0, signedAt, token, ipHash)
    .run();

  const emailing = Boolean(email && env.RESEND_API_KEY && env.EMAIL_FROM);
  if (emailing) ctx.waitUntil(sendConfirmation(env, { name, email, city, isPublic, signedAt, token }));

  const countRow = await env.DB.prepare('SELECT COUNT(*) AS n FROM signatures').first<{ n: number }>();
  return json({ ok: true, signedAt, count: countRow?.n ?? null, emailQueued: emailing });
}

// ---------- POST /api/petition/remove ----------

async function remove(request: Request, env: Env): Promise<Response> {
  if (!env.DB) return json({ error: 'Not available yet.' }, 503);
  const body = await readBody(request);
  const token = clean(body?.token, 100);
  if (token.length < 20) return json({ error: 'This link is not valid.' }, 400);
  const res = await env.DB.prepare('DELETE FROM signatures WHERE manage_token = ?1').bind(token).run();
  if (!res.meta?.changes) return json({ error: 'We could not find that signature. It may already have been removed.' }, 404);
  return json({ ok: true });
}

// ---------- GET /api/petition/export ----------
// Used by the Google Apps Script in google-sheet/ to refresh the signer sheet daily.

async function exportAll(request: Request, env: Env): Promise<Response> {
  const auth = request.headers.get('authorization') || '';
  if (!env.EXPORT_TOKEN || auth !== `Bearer ${env.EXPORT_TOKEN}`) return json({ error: 'Unauthorized' }, 401);
  if (!env.DB) return json({ error: 'No database' }, 503);
  const rows = await env.DB.prepare(
    `SELECT id, name, email, city, state, zip, affiliation, comment, heard_from, is_public, wants_updates, signed_at
     FROM signatures ORDER BY id ASC`,
  ).all<Record<string, unknown>>();
  return json({
    exportedAt: new Date().toISOString(),
    signers: rows.results.map((r) => ({
      id: r.id,
      name: r.name,
      signedAt: r.signed_at,
      public: r.is_public === 1,
      email: r.email,
      city: r.city,
      state: r.state,
      zip: r.zip,
      affiliation: r.affiliation ? AFFILIATIONS[String(r.affiliation)] ?? r.affiliation : null,
      heardFrom: r.heard_from ? HEARD_FROM[String(r.heard_from)] ?? r.heard_from : null,
      comment: r.comment,
      wantsUpdates: r.wants_updates === 1,
    })),
  });
}

// ---------- Email ----------

async function sendConfirmation(
  env: Env,
  s: { name: string; email: string; city: string | null; isPublic: boolean; signedAt: string; token: string },
): Promise<void> {
  if (!env.RESEND_API_KEY || !env.EMAIL_FROM || !env.DB) return;
  const siteUrl = (env.SITE_URL || 'https://evaxie.us').replace(/\/$/, '');
  const removeUrl = `${siteUrl}/petition/remove/?t=${encodeURIComponent(s.token)}`;
  const when = new Date(s.signedAt).toLocaleString('en-US', {
    timeZone: 'America/New_York', dateStyle: 'long', timeStyle: 'short',
  }) + ' ET';
  const visibility = s.isPublic
    ? `Your name${s.city ? ' and city' : ''} will appear on the public list of signers at ${siteUrl}/petition/.`
    : 'You chose to keep your signature private. It counts toward the total, but your name will not be shown.';
  const replyTo = env.EMAIL_REPLY_TO || 'weare@geodesic.pro';

  const text = [
    `Dear ${s.name},`,
    '',
    'Thank you for signing the petition for fair treatment for Eva Xie, reform of how ICE interacts with the public, and mutual respect between all people and countries, especially the United States and China.',
    '',
    `Signed: ${when}`,
    visibility,
    '',
    `Please share the petition: ${siteUrl}/petition/`,
    '',
    `If you did not sign, or want to remove your signature, use this link: ${removeUrl}`,
    `Questions? Reply to this email or write to ${replyTo}.`,
    '',
    'Free Eva · 釋放謝翌',
    'Firm, lawful, respectful.',
  ].join('\n');

  const html = `<!doctype html><html><body style="margin:0;background:#f7f5f2;font-family:Arial,Helvetica,sans-serif;color:#151515">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f7f5f2;padding:24px 0"><tr><td align="center">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;background:#ffffff;border-top:6px solid #e77500">
<tr><td style="padding:28px 28px 8px">
<p style="margin:0 0 4px;font-size:13px;letter-spacing:2px;text-transform:uppercase;color:#e77500;font-weight:bold">Free Eva · 釋放謝翌</p>
<h1 style="margin:0 0 16px;font-size:24px;line-height:1.2">Thank you for signing.</h1>
<p style="margin:0 0 14px;font-size:16px;line-height:1.55">Dear ${esc(s.name)},</p>
<p style="margin:0 0 14px;font-size:16px;line-height:1.55">Thank you for signing the petition for fair treatment for Eva Xie, reform of how ICE interacts with the public, and mutual respect between all people and countries, especially the United States and China.</p>
<p style="margin:0 0 6px;font-size:15px;line-height:1.55"><strong>Signed:</strong> ${esc(when)}</p>
<p style="margin:0 0 20px;font-size:15px;line-height:1.55;color:#444">${esc(visibility)}</p>
<p style="margin:0 0 24px"><a href="${siteUrl}/petition/" style="display:inline-block;background:#e77500;color:#151515;text-decoration:none;font-weight:bold;padding:12px 18px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;font-size:14px">Share the petition</a></p>
</td></tr>
<tr><td style="padding:16px 28px 24px;border-top:1px solid #eee;font-size:13px;line-height:1.5;color:#666">
If you did not sign, or want to remove your signature, <a href="${removeUrl}" style="color:#b35a00">remove it here</a>.<br>
Questions? Reply to this email or write to <a href="mailto:${esc(replyTo)}" style="color:#b35a00">${esc(replyTo)}</a>.<br><br>
Firm, lawful, respectful. 中美相互尊重
</td></tr></table></td></tr></table></body></html>`;

  let error: string | null = null;
  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, 'content-type': 'application/json' },
      body: JSON.stringify({
        from: env.EMAIL_FROM,
        to: [s.email],
        reply_to: replyTo,
        subject: 'Thank you for signing the Free Eva petition',
        text,
        html,
      }),
    });
    if (!res.ok) error = `${res.status} ${(await res.text()).slice(0, 300)}`;
  } catch (err) {
    error = String(err).slice(0, 300);
  }
  await env.DB.prepare('UPDATE signatures SET email_sent_at = ?1, email_error = ?2 WHERE manage_token = ?3')
    .bind(error ? null : new Date().toISOString(), error, s.token)
    .run();
  if (error) console.error('confirmation email failed', error);
}

// ---------- helpers ----------

async function verifyTurnstile(secret: string, token: string, ip: string): Promise<boolean> {
  if (!token) return false;
  const form = new FormData();
  form.append('secret', secret);
  form.append('response', token);
  if (ip) form.append('remoteip', ip);
  const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
  const data = (await res.json()) as { success?: boolean };
  return Boolean(data.success);
}

async function readBody(request: Request): Promise<Record<string, unknown> | null> {
  try {
    const type = request.headers.get('content-type') || '';
    if (type.includes('application/json')) return (await request.json()) as Record<string, unknown>;
    const form = await request.formData();
    return Object.fromEntries(form.entries());
  } catch {
    return null;
  }
}

function clean(v: unknown, max: number): string {
  if (typeof v !== 'string') return '';
  // Drop control characters and collapse whitespace.
  return v.replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max);
}

function cleanMultiline(v: unknown, max: number): string {
  if (typeof v !== 'string') return '';
  return v.replace(/\r\n?/g, '\n').replace(/[\u0000-\u0009\u000b-\u001f\u007f]/g, ' ').replace(/\n{3,}/g, '\n\n').trim().slice(0, max);
}

function truthy(v: unknown): boolean {
  return v === true || v === 'on' || v === 'true' || v === '1' || v === 1;
}

function esc(s: string): string {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);
}

async function sha256(s: string): Promise<string> {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function randomToken(): string {
  const bytes = crypto.getRandomValues(new Uint8Array(24));
  return [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function json(data: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers },
  });
}
