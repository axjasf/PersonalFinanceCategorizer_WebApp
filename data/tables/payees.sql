CREATE TABLE payees (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE payee_mapping (
    id INTEGER PRIMARY KEY,
    payee_standard_id INTEGER NOT NULL,  -- The standardized payee
    payee_variant TEXT NOT NULL UNIQUE,  -- The variant payee name
    FOREIGN KEY (payee_standard_id) REFERENCES payees(id)
);