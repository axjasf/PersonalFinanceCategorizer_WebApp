CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    transaction_date DATE NOT NULL,
    total_amount REAL NOT NULL,
    payee_id INTEGER,
    category_id INTEGER,
    account_id INTEGER,
    description TEXT,
    FOREIGN KEY (payee_id) REFERENCES payees(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE transaction_splits (
    id INTEGER PRIMARY KEY,
    transaction_id INTEGER NOT NULL,   -- References the transaction
    category_id INTEGER NOT NULL,      -- Category for this split
    split_amount REAL NOT NULL,        -- Amount for this category
    split_index INTEGER,               -- Order in which the split was inserted
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);


