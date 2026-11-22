-- Makes email optional and adds optional signer fields.
-- The Worker applies this automatically on its first request after deploy (see ensureSchema in
-- worker/index.ts), so you normally do not need to run it. It is kept here as the record of the schema.
CREATE TABLE IF NOT EXISTS signatures_v2 (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  name            TEXT    NOT NULL,
  email           TEXT    UNIQUE,              -- optional; stored lowercased; never shown publicly
  city            TEXT,
  state           TEXT,                        -- optional, 2-letter US state or other region
  zip             TEXT,                        -- optional
  affiliation     TEXT,                        -- optional: student | faculty_staff | alum | community | unaffiliated
  comment         TEXT,                        -- optional "why I'm signing", never shown automatically
  heard_from      TEXT,                        -- optional: qr | social | rally | friend | news | email | other
  is_public       INTEGER NOT NULL DEFAULT 0,
  wants_updates   INTEGER NOT NULL DEFAULT 0,
  signed_at       TEXT    NOT NULL,
  manage_token    TEXT    NOT NULL UNIQUE,
  ip_hash         TEXT,
  email_sent_at   TEXT,
  email_error     TEXT
);
INSERT INTO signatures_v2 (id, name, email, city, is_public, wants_updates, signed_at, manage_token, ip_hash, email_sent_at, email_error)
  SELECT id, name, email, city, is_public, wants_updates, signed_at, manage_token, ip_hash, email_sent_at, email_error FROM signatures;
DROP TABLE signatures;
ALTER TABLE signatures_v2 RENAME TO signatures;
CREATE INDEX IF NOT EXISTS idx_signatures_public ON signatures (is_public, signed_at DESC);
CREATE INDEX IF NOT EXISTS idx_signatures_ip ON signatures (ip_hash, signed_at);
