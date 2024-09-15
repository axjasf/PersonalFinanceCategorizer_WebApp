-- Accounts Table
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    institution TEXT
);

-- Categories Table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    parent_id INTEGER,
    FOREIGN KEY(parent_id) REFERENCES categories(id)
);

-- Payees Table
CREATE TABLE payees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
