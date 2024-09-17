CREATE TRIGGER delete_account_cascade
BEFORE DELETE ON accounts
FOR EACH ROW
BEGIN
    -- Delete associated transactions
    DELETE FROM transactions WHERE account_id = OLD.id;
    
    -- Delete associated transaction splits
    DELETE FROM transaction_splits WHERE transaction_id IN (SELECT id FROM transactions WHERE account_id = OLD.id);
END;