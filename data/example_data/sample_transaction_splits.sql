-- Transaction 1 ($150.50 total, split into 2 categories)
INSERT INTO transaction_splits (transaction_id, category_id, split_amount, split_index) 
VALUES
    (1, 10, 100.00, 1),  -- Electronics
    (1, 10, 50.50, 2);   -- Clothing

-- Transaction 2 ($50.00 total, split into 2 categories)
INSERT INTO transaction_splits (transaction_id, category_id, split_amount, split_index) 
VALUES
    (2, 1, 30.00, 1),  -- Groceries
    (2, 6, 20.00, 2);  -- Transportation

-- Transaction 3 ($85.30 total, split into 3 categories)
INSERT INTO transaction_splits (transaction_id, category_id, split_amount, split_index) 
VALUES
    (3, 8, 50.30, 1),  -- Healthcare
    (3, 6, 20.00, 2),  -- Transportation
    (3, 9, 15.00, 3);  -- Subscriptions

-- Transaction 4 ($75.10 total, split into 2 categories)
INSERT INTO transaction_splits (transaction_id, category_id, split_amount, split_index) 
VALUES
    (4, 1, 45.10, 1),  -- Groceries
    (4, 2, 30.00, 2);  -- Dining Out

-- Repeat similar insertions for 25 total split transactions, adjusting transaction IDs and amounts accordingly
