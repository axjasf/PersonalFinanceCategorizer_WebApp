-- Payees Table (modified)
CREATE TABLE payees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Payee Variants Table
CREATE TABLE payee_variants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    payee_id INTEGER NOT NULL,
    FOREIGN KEY (payee_id) REFERENCES payees(id)
);
