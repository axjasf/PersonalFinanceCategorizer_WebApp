import pytest
from services.data_operations import get_transactions, get_transaction_splits, get_accounts, add_account, update_account, delete_account, AccountAlreadyExistsError
from database.db_utils import init_db, get_session
from sqlalchemy import text
import pandas as pd

@pytest.fixture
def setup_database():
    from database.db_utils import init_db
    init_db()
    yield
    # Clean up code here if needed

class InvalidAccountError(Exception):
    """Raised when an operation is attempted on an invalid account."""
    pass

def test_get_transactions(setup_database):
    transactions = get_transactions()
    assert isinstance(transactions, pd.DataFrame)
    assert 'id' in transactions.columns
    assert 'transaction_date' in transactions.columns

def test_get_transaction_splits(setup_database):
    # First, add a transaction and a split
    session = get_session()
    session.execute(text("INSERT INTO transactions (transaction_date, amount, description) VALUES ('2023-01-01', 100.0, 'Test Transaction')"))
    session.execute(text("INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES (1, 1, 100.0)"))
    session.commit()

    splits = get_transaction_splits(1)
    assert isinstance(splits, pd.DataFrame)
    assert 'id' in splits.columns
    assert 'allocated_amount' in splits.columns

def test_get_accounts(setup_database):
    accounts = get_accounts()
    assert isinstance(accounts, pd.DataFrame)
    assert 'id' in accounts.columns
    assert 'name' in accounts.columns

def test_add_account(setup_database):
    # Use a unique name for this test
    result = add_account("Test Account 1", "Checking", "Test Bank")
    assert result is not None  # Or any other appropriate assertion

def test_add_duplicate_account(setup_database):
    # Add an account
    add_account("Unique Account 1", "Savings", "Another Bank")
    
    # Try to add the same account again
    with pytest.raises(AccountAlreadyExistsError):
        add_account("Unique Account 1", "Savings", "Another Bank")

def test_update_account(setup_database):
    # First, add an account
    add_account("Test Account", "Checking", "Test Bank")
    
    # Get the account ID
    session = get_session()
    result = session.execute(text("SELECT id FROM accounts WHERE name = 'Test Account'"))
    account_id = result.fetchone()[0]
    
    # Update the account
    update_account(account_id, "Updated Account", "Savings", "New Bank")
    
    # Verify the update
    result = session.execute(text("SELECT * FROM accounts WHERE id = :id"), {"id": account_id})
    updated_account = result.fetchone()
    assert updated_account['name'] == "Updated Account"
    assert updated_account['type'] == "Savings"
    assert updated_account['institution'] == "New Bank"

def test_delete_account(setup_database):
    # First, add an account
    add_account("Test Account", "Checking", "Test Bank")
    
    # Get the account ID
    session = get_session()
    result = session.execute(text("SELECT id FROM accounts WHERE name = 'Test Account'"))
    account_id = result.fetchone()[0]
    
    # Delete the account
    delete_account(account_id)
    
    # Verify the deletion
    result = session.execute(text("SELECT * FROM accounts WHERE id = :id"), {"id": account_id})
    assert result.fetchone() is None

def test_invalid_account_update(setup_database):
    with pytest.raises(InvalidAccountError):
        update_account(999, "Invalid Account", "Invalid", "Invalid Bank")

def test_invalid_account_delete(setup_database):
    with pytest.raises(InvalidAccountError):
        delete_account(999)
