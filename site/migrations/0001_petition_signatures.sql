-- Petition signatures for evaxie.us.
-- Apply once: Cloudflare dashboard > D1 > free-eva-petition > Console (paste this file),
-- or `npx wrangler d1 migrations apply free-eva-petition --remote` from /site.
CREATE TABLE IF NOT EXISTS signatures (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  name            TEXT    NOT NULL,
  email           TEXT    NOT NULL UNIQUE,   -- stored lowercased; never shown publicly
  city            TEXT,                       -- optional, shown only if is_public = 1
  is_public       INTEGER NOT NULL DEFAULT 0, -- 1 = show name (and city) on the site
  wants_updates   INTEGER NOT NULL DEFAULT 0, -- 1 = ok to email campaign updates
  signed_at       TEXT    NOT NULL,           -- ISO 8601 UTC time of signing
  manage_token    TEXT    NOT NULL UNIQUE,    -- secret token for the "remove my signature" link
  ip_hash         TEXT,                       -- salted SHA-256 of the IP, for rate limiting only
  email_sent_at   TEXT,                       -- when the confirmation email went out
  email_error     TEXT                        -- last error from the email provider, if any
);

CREATE INDEX IF NOT EXISTS idx_signatures_public ON signatures (is_public, signed_at DESC);
CREATE INDEX IF NOT EXISTS idx_signatures_ip ON signatures (ip_hash, signed_at);
