# Petition setup (evaxie.us/petition/)

The Petition tab is a static page plus a small Worker API (`worker/index.ts`) that stores
signatures in Cloudflare D1 and sends a confirmation email through Resend.

Until step 1 is done, the page shows the petition text and "Online signing opens soon".
Steps 2 and 3 are optional: without them signing still works, there is just no spam check
(step 2) or no confirmation email (step 3).

## What gets stored
One row per signature in the `signatures` table: name, email (lowercased), optional city/school,
public or private choice, whether they want campaign updates, signing time (UTC), a secret
removal token, a salted hash of the IP (rate limiting only), and email delivery status.
The public list shows **only** name, city and time, and **only** for people who chose "Publicly".
Emails are never exposed by the API.

## 1. Database (required)
1. Cloudflare dashboard > Storage & Databases > D1 > **Create database**, name `free-eva-petition`.
2. Open it > **Console**, paste the contents of `migrations/0001_petition_signatures.sql`, run it.
3. Copy the database ID, then in `wrangler.jsonc` uncomment the `d1_databases` block and paste the ID.
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
