INSERT INTO payees (id, name) VALUES 
    (1, 'Amazon'),
    (2, 'Walmart'),
    (3, 'Netflix'),
    (4, 'Spotify'),
    (5, 'Apple Store'),
    (6, 'Starbucks'),
    (7, 'Shell Gas Station'),
    (8, 'Uber'),
    (9, 'Whole Foods'),
    (10, 'Target'),
    (11, 'Best Buy'),
    (12, 'Disney Plus'),
    (13, 'Rent Payment'),
    (14, 'Health Clinic'),
    (15, 'Subway');


INSERT INTO payee_variants (id, payee_standard_id, payee_variant) 
VALUES
    (1, 1, 'Amazon Grocery'),         -- Maps to 'Amazon'
    (2, 1, 'Amazon.de'),              -- Maps to 'Amazon'
    (3, 1, 'Amazon UK'),              -- Maps to 'Amazon'
    (4, 6, 'Starbucks Coffee'),       -- Maps to 'Starbucks'
    (5, 6, 'Starbucks NYC'),          -- Maps to 'Starbucks'
    (6, 2, 'Walmart Supercenter'),    -- Maps to 'Walmart'
    (7, 2, 'Walmart Neighborhood'),   -- Maps to 'Walmart'
    (9, 3, 'Netflix Subscription'),   -- Maps to 'Netflix'
    (10, 3, 'Netflix Services');      -- Maps to 'Netflix'
