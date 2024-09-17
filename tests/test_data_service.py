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
    success, message = create_account("New Test Account", "Savings", "Test Bank")
    assert success
    assert "successfully" in message

    # Try to create a duplicate account
    success, message = create_account("New Test Account", "Checking", "Another Bank")
    assert not success
    assert "already exists" in message

def test_load_transactions_caching(setup_database, monkeypatch):
    # Mock the expensive operation
    mock_data = pd.DataFrame({'id': [1, 2], 'amount': [100, 200]})
    mock_get_transactions = lambda: mock_data
    monkeypatch.setattr('services.data_service.get_transactions', mock_get_transactions)
    
    # First call should execute the function
    result1 = load_transactions()
    assert result1.equals(mock_data)
    
    # Second call should return cached result
    result2 = load_transactions()
    assert result2.equals(mock_data)
    
    # We can't directly check cache hits, so we'll check if the function returns the same object
    assert result1 is result2

def test_database_connection_error(monkeypatch):
    def mock_get_transactions():
        raise DatabaseConnectionError("Database connection error")
    
    monkeypatch.setattr('services.data_service.get_transactions', mock_get_transactions)
    
    with pytest.raises(DatabaseConnectionError):
        load_transactions()
