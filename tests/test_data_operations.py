import pytest
from services.data_operations import get_transactions, get_transaction_splits, get_accounts, add_account, update_account, delete_account, AccountAlreadyExistsError
from database.db_utils import init_db, get_session
from sqlalchemy import text
import pandas as pd
import uuid

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
    # Generate a unique account name
    unique_name = f"Test Account {uuid.uuid4().hex[:8]}"
    
    # Test successful account addition
    result = add_account(unique_name, "Checking", "Test Bank")
    assert result is not None, "Account should be added successfully"
    
    # Test adding an account with the same name (should raise an error)
    with pytest.raises(AccountAlreadyExistsError):
        add_account(unique_name, "Savings", "Another Bank")

    # Test adding another unique account
    another_unique_name = f"Another Account {uuid.uuid4().hex[:8]}"
    another_result = add_account(another_unique_name, "Savings", "Another Bank")
    assert another_result is not None, "Second unique account should be added successfully"

def test_add_duplicate_account(setup_database):
    # Generate a unique account name
    unique_name = f"Unique Account {uuid.uuid4().hex[:8]}"
    
    # Add an account
    add_account(unique_name, "Savings", "Another Bank")
    
    # Try to add the same account again
    with pytest.raises(AccountAlreadyExistsError, match=f"An account with the name '{unique_name}' already exists"):
        add_account(unique_name, "Savings", "Another Bank")
