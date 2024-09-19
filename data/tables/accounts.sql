-- Accounts Table
CREATE TABLE IF NOT EXISTS "accounts" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"type"	TEXT NOT NULL,
	"institution"	TEXT,
    "bank_identifier" TEXT UNIQUE,
	PRIMARY KEY("id")
);