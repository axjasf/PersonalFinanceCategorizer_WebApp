-- Transactions Table
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    transaction_date DATE NOT NULL,
    amount REAL NOT NULL,
    payee_id INTEGER,
    account_id INTEGER,
    description TEXT,
    FOREIGN KEY(account_id) REFERENCES accounts(id),
    FOREIGN KEY(payee_id) REFERENCES payees(id)
);

-- Transaction Splits Table
CREATE TABLE transaction_splits (
    id INTEGER PRIMARY KEY,
    transaction_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    allocated_amount REAL NOT NULL,
    FOREIGN KEY(transaction_id) REFERENCES transactions(id),
    FOREIGN KEY(category_id) REFERENCES categories(id)
);
