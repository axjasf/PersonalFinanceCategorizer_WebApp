CREATE VIEW vw_transactions_with_details AS
SELECT 
    t.id,
    t.transaction_date,
    t.amount,
    t.payee_id,
    t.account_id,
    t.description,
    a.name as account_name,
    p.name as payee_name
FROM 
    transactions t
LEFT JOIN 
    accounts a ON t.account_id = a.id
LEFT JOIN 
    payees p ON t.payee_id = p.id;