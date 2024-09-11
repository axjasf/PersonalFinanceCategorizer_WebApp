CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL,  -- e.g., Savings, Checking, Credit
    institution TEXT     -- New column for financial institution
);

