BEGIN TRANSACTION;

-- Insert Categories
INSERT INTO categories (id, name, parent_id) VALUES
    (1, 'Groceries', NULL),
    (2, 'Household', NULL),
    (3, 'Clothing', NULL),
    (4, 'Electronics', NULL),
    (5, 'Entertainment', NULL),
    (6, 'Subscriptions', 5);

-- Insert Payees
INSERT INTO payees (id, name) VALUES
    (1, 'Amazon'),
    (2, 'Netflix'),
    (3, 'Corner Store'),
    (4, 'Whole Foods');

-- Insert Accounts
INSERT INTO accounts (id, name, type, institution) VALUES
    (1, 'Checking Account', 'Bank Account', 'Bank A'),
    (2, 'Credit Card', 'Credit Card', 'Bank B');
	
COMMIT;
