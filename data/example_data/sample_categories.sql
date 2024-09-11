INSERT INTO categories (name) VALUES 
    ('Groceries'),
    ('Dining Out'),
    ('Entertainment'),
    ('Utilities'),
    ('Rent'),
    ('Transportation'),
    ('Fuel'),
    ('Healthcare'),
    ('Subscriptions'),
    ('Shopping');

-- Add subcategories (parent-child relationships)
INSERT INTO categories (name, parent_id) VALUES 
    ('Streaming Services', 9),  -- Subcategory of Subscriptions
    ('Clothing', 10),           -- Subcategory of Shopping
    ('Electronics', 10);        -- Subcategory of Shopping
