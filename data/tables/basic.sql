-- Accounts Table
CREATE TABLE IF NOT EXISTS "accounts" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"type"	TEXT NOT NULL,
	"institution"	TEXT,
    "bank_identifier" TEXT UNIQUE,
	PRIMARY KEY("id")
);


-- Categories Table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    parent_id INTEGER,
    FOREIGN KEY(parent_id) REFERENCES categories(id)
);
