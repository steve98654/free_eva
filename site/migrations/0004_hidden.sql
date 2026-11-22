-- Lets the campaign hide a public name (spam or abuse) without deleting the signature.
-- Applied automatically by the Worker (ensureSchema); kept as a record.
ALTER TABLE signatures ADD COLUMN hidden INTEGER NOT NULL DEFAULT 0;
