# Petition setup (evaxie.us/petition/)

The Petition tab is a static page plus a small Worker API (`worker/index.ts`) that stores
signatures in Cloudflare D1 and sends a confirmation email through Resend.

Until step 1 is done, the page shows the petition text and "Online signing opens soon".
Steps 2 and 3 are optional: without them signing still works, there is just no spam check
(step 2) or no confirmation email (step 3).

## What gets stored
One row per signature in the `signatures` table. Required: name and signing time (UTC, set
automatically). Optional: email (lowercased), city, state, ZIP, Princeton connection, how they heard,
"why I'm signing" comment, whether they want campaign updates. Also stored: public or private choice,
a secret removal token, a salted hash of the IP (rate limiting and duplicate checks only), and email
delivery status.

The Worker creates and upgrades the table itself on its first request after a deploy (`ensureSchema`
in `worker/index.ts`), so schema changes need no manual SQL. `migrations/` records each version.

Duplicates: one signature per email. Without an email, the same name can't sign twice from the same
network. Turnstile (step 2) matters more now that email is optional.
The public list shows **only** name, city and time, and **only** for people who chose "Publicly".
Emails are never exposed by the API.

## 1. Database (required)
1. Cloudflare dashboard > Storage & Databases > D1 > **Create database**, name `free-eva-petition`.
2. Open it > **Console**, paste the contents of `migrations/0001_petition_signatures.sql`, run it.
3. Copy the database ID into the `d1_databases` block in `wrangler.jsonc` (done: free-eva-petition is connected).
   Commit to the production branch; Workers Builds redeploys.

## 2. Spam check with Turnstile (recommended)
1. Dashboard > Turnstile > **Add widget**, hostname `evaxie.us`, mode Managed.
2. Put the **site key** in `wrangler.jsonc` > `vars.TURNSTILE_SITE_KEY` (it is public).
3. Worker `free-eva` > Settings > Variables and Secrets > add **Secret** `TURNSTILE_SECRET_KEY`.

## 3. Confirmation email with Resend
1. Create an account at resend.com > Domains > **Add domain** `evaxie.us`, and add the DNS records it
   shows (in Cloudflare DNS). Wait for "Verified".
2. Resend > API Keys > create a key with "Sending access".
3. Worker `free-eva` > Settings > Variables and Secrets > add **Secret** `RESEND_API_KEY`.
4. Optional: add **Secret** `IP_SALT` with any long random string.

Emails come from `EMAIL_FROM` (`Free Eva <petition@evaxie.us>`) with replies going to
`EMAIL_REPLY_TO` (`weare@geodesic.pro`); change them in `wrangler.jsonc` > `vars`.

## 4. Daily Google Sheet of signers
`google-sheet/petition-sync.gs` is a Google Apps Script that pulls every signer from
`/api/petition/export` and rewrites a "Signers" tab once a day (name, date, time, public?, city,
state, ZIP, Princeton connection, how they heard, comment, wants updates). Emails are left out
unless you set `INCLUDE_EMAIL = true` in the script.
1. Worker `free-eva` > Settings > Variables and Secrets > add **Secret** `EXPORT_TOKEN` with a long
   random string. The export endpoint is off until this exists.
2. Open the Google Sheet > Extensions > Apps Script, paste the script, add Script Property
   `EXPORT_TOKEN` with the same string, then run `setup` once and approve.

## Reading the signatures
Dashboard > D1 > `free-eva-petition` > Console, for example:

```sql
SELECT COUNT(*) FROM signatures;
SELECT name, email, city, is_public, wants_updates, signed_at FROM signatures ORDER BY signed_at DESC;
SELECT name, email, email_error FROM signatures WHERE email_sent_at IS NULL;  -- emails that failed
```

Export to CSV from the command line: `npx wrangler d1 export free-eva-petition --remote --output petition.sql`
or run a query with `--json`.

## Testing locally
```sh
cd site && npm run build
# copy wrangler.jsonc to wrangler.test.jsonc, uncomment d1_databases with any placeholder ID, then:
npx wrangler d1 migrations apply free-eva-petition --local -c wrangler.test.jsonc
npx wrangler dev -c wrangler.test.jsonc
```
