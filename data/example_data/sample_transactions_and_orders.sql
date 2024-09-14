BEGIN TRANSACTION;
-- Insert Orders and Items

-- Order 1: Single Transaction, Single Category
INSERT INTO orders (order_id, order_date, total_amount, payee_id) VALUES
    ('A1001', '2023-01-15', 500.00, 1);

INSERT INTO order_items (order_id, item_description, category_id, item_price, quantity) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1001'), 'Grocery Item', 1, 5.00, 100);

-- Order 2: Multiple Transactions, Single Category
INSERT INTO orders (order_id, order_date, total_amount, payee_id) VALUES
    ('A1002', '2023-02-20', 200.00, 1);

INSERT INTO order_items (order_id, item_description, category_id, item_price, quantity) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1002'), 'Clothing Item', 3, 40.00, 5);

-- Order 3: Multiple Transactions, Multiple Categories
INSERT INTO orders (order_id, order_date, total_amount, payee_id) VALUES
    ('A1003', '2023-03-25', 300.00, 1);

-- Clothing Items
INSERT INTO order_items (order_id, item_description, category_id, item_price, quantity) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1003'), 'Clothing Item', 3, 40.00, 5);

-- Household Items
INSERT INTO order_items (order_id, item_description, category_id, item_price, quantity) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1003'), 'Household Item', 2, 20.00, 3);

-- Insert Transactions and Splits

-- Transactions for Order 1
INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description) VALUES
    ('2023-01-16', 500.00, 1, 1, 'Amazon Order A1001');

INSERT INTO order_payments (order_id, transaction_id, payment_amount) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1001'), 
     (SELECT id FROM transactions WHERE description = 'Amazon Order A1001'), 
     500.00);

INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1001'), 1, 500.00);

-- Transactions for Order 2
-- Transaction 1
INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description) VALUES
    ('2023-02-21', 120.00, 1, 1, 'Amazon Order A1002 - Part 1');

INSERT INTO order_payments (order_id, transaction_id, payment_amount) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1002'), 
     (SELECT id FROM transactions WHERE description = 'Amazon Order A1002 - Part 1'), 
     120.00);

INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1002 - Part 1'), 3, 120.00);

-- Transaction 2
INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description) VALUES
    ('2023-02-22', 80.00, 1, 1, 'Amazon Order A1002 - Part 2');

INSERT INTO order_payments (order_id, transaction_id, payment_amount) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1002'), 
     (SELECT id FROM transactions WHERE description = 'Amazon Order A1002 - Part 2'), 
     80.00);

INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1002 - Part 2'), 3, 80.00);

-- Transactions for Order 3
-- Category Totals
-- Clothing: 5 items * $40 = $200
-- Household: 3 items * $20 = $60
-- Total: $260 (Note: Adjusted to match total transaction amounts)

-- Category Percentages
-- Clothing: $200 / $260 ≈ 76.92%
-- Household: $60 / $260 ≈ 23.08%

-- Transactions and Allocations
-- Transaction 1: $100
INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description) VALUES
    ('2023-03-26', 100.00, 1, 1, 'Amazon Order A1003 - Part 1');

INSERT INTO order_payments (order_id, transaction_id, payment_amount) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1003'), 
     (SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 1'), 
     100.00);

INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 1'), 3, 76.92),
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 1'), 2, 23.08);

-- Transaction 2: $50
INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description) VALUES
    ('2023-03-27', 50.00, 1, 1, 'Amazon Order A1003 - Part 2');

INSERT INTO order_payments (order_id, transaction_id, payment_amount) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1003'), 
     (SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 2'), 
     50.00);

INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 2'), 3, 38.46),
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 2'), 2, 11.54);

-- Transaction 3: $80
INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description) VALUES
    ('2023-03-28', 80.00, 1, 1, 'Amazon Order A1003 - Part 3');

INSERT INTO order_payments (order_id, transaction_id, payment_amount) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1003'), 
     (SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 3'), 
     80.00);

INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 3'), 3, 61.54),
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 3'), 2, 18.46);

-- Transaction 4: $70
INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description) VALUES
    ('2023-03-29', 70.00, 1, 1, 'Amazon Order A1003 - Part 4');

INSERT INTO order_payments (order_id, transaction_id, payment_amount) VALUES
    ((SELECT id FROM orders WHERE order_id = 'A1003'), 
     (SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 4'), 
     70.00);

INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 4'), 3, 53.84),
    ((SELECT id FROM transactions WHERE description = 'Amazon Order A1003 - Part 4'), 2, 16.16);

-- Non-Amazon Transactions

-- Netflix Subscription
INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description) VALUES
    ('2023-04-05', 15.00, 2, 1, 'Netflix Subscription');

INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES
    ((SELECT id FROM transactions WHERE description = 'Netflix Subscription'), 6, 15.00);

-- Corner Store Purchase
INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description) VALUES
    ('2023-04-10', 50.00, 3, 1, 'Corner Store Purchase');

INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES
    ((SELECT id FROM transactions WHERE description = 'Corner Store Purchase'), 1, 30.00),
    ((SELECT id FROM transactions WHERE description = 'Corner Store Purchase'), 2, 20.00);

COMMIT;
