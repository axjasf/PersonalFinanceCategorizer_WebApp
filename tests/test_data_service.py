import pytest
from services.data_service import load_transactions, load_splits, load_accounts, create_account
import pandas as pd
import streamlit as st

class DatabaseConnectionError(Exception):
    """Raised when there's an issue connecting to the database."""
    pass

@pytest.fixture
def setup_database():
    from database.db_utils import init_db
    init_db()
    yield
    # Clean up code here if needed

def test_load_transactions(setup_database):
    transactions = load_transactions()
    assert isinstance(transactions, pd.DataFrame)
    assert 'id' in transactions.columns

def test_load_splits(setup_database):
    # Assuming we have a transaction with id 1 from the setup
    splits = load_splits(1)
    assert isinstance(splits, pd.DataFrame)
    assert 'id' in splits.columns

def test_load_accounts(setup_database):
    accounts = load_accounts()
    assert isinstance(accounts, pd.DataFrame)
    assert 'id' in accounts.columns

def test_create_account(setup_database):
    # Generate a unique account name
    unique_name = f"Test Account {uuid.uuid4().hex[:8]}"
    
    # Create the account
    success, message = create_account(unique_name, "Savings", "Test Bank")
    assert success, f"Failed to create account: {message}"
    assert "successfully" in message, f"Unexpected success message: {message}"

    # Try to create a duplicate account
    success, message = create_account("New Test Account", "Checking", "Another Bank")
    assert not success
    assert "already exists" in message

def test_database_connection_error(monkeypatch):
    def mock_get_transactions():
        raise DatabaseConnectionError("Database connection error")
    
    monkeypatch.setattr('services.data_service.get_transactions', mock_get_transactions)
    
    with pytest.raises(DatabaseConnectionError):
        load_transactions()
