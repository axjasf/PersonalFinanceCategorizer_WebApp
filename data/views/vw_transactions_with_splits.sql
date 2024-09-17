-- Drop the view if it exists
DROP VIEW IF EXISTS vw_transactions_with_splits;

-- Create the view
CREATE VIEW vw_transactions_with_splits AS
SELECT 
    t.id AS transaction_id,
    t.transaction_date,
    t.amount AS transaction_amount,
    ts.allocated_amount AS split_amount,
    c.name AS category_name,
    p.name AS payee_name,
    a.name AS account_name,
    t.description
FROM 
    transactions t
LEFT JOIN 
    transaction_splits ts ON t.id = ts.transaction_id
LEFT JOIN 
    categories c ON ts.category_id = c.id
LEFT JOIN 
    payees p ON t.payee_id = p.id
LEFT JOIN 
    accounts a ON t.account_id = a.id;

