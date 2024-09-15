-- Orders Table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    order_id TEXT NOT NULL UNIQUE,
    order_date DATE NOT NULL,
    total_amount REAL NOT NULL,
    payee_id INTEGER NOT NULL,
    FOREIGN KEY(payee_id) REFERENCES payees(id)
);

-- Order Items Table
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    item_description TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    item_price REAL NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

-- Order Payments Table
CREATE TABLE order_payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    transaction_id INTEGER NOT NULL,
    payment_amount REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(transaction_id) REFERENCES transactions(id)
);
