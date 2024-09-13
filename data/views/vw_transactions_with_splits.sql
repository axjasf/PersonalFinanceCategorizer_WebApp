CREATE VIEW vw_transactions_with_splits AS
SELECT 
    t.id AS transaction_id,
    t.transaction_date,
    t.total_amount,
    ts.split_amount,
    ts.split_index,
    ts.description AS split_description,
    c.name AS category_name,
    p.name AS payee_name,
    a.name AS account_name
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
