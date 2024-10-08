import pytest
from services.data_service import load_transactions, load_splits, load_accounts, create_account
import pandas as pd
import streamlit as st
import uuid

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
    unique_identifier = f"bank_{uuid.uuid4().hex[:8]}"
    
    # Create the account
    result = create_account(unique_name, "Savings", "Test Bank", unique_identifier)
    
    # Check if the result is a tuple with three elements (success, message, bank_identifier)
    assert isinstance(result, tuple) and len(result) == 3, f"Expected (success, message, bank_identifier), got {result}"
    
    success, message, returned_bank_identifier = result
    assert success, f"Failed to create account: {message}"
    assert "successfully" in message.lower(), f"Unexpected success message: {message}"
    assert returned_bank_identifier == unique_identifier, f"Bank identifier mismatch: expected {unique_identifier}, got {returned_bank_identifier}"

    # Try to create a duplicate account
    result = create_account(unique_name, "Checking", "Another Bank", f"bank_{uuid.uuid4().hex[:8]}")
    assert isinstance(result, tuple) and len(result) == 3, f"Expected (success, message, bank_identifier), got {result}"
    
    success, message, _ = result
    assert not success, "Should not be able to create duplicate account"
    assert "already exists" in message.lower(), f"Unexpected error message: {message}"

    # Try to create an account with duplicate bank identifier
    different_name = f"Different Account {uuid.uuid4().hex[:8]}"
    result = create_account(different_name, "Checking", "Another Bank", unique_identifier)
    assert isinstance(result, tuple) and len(result) == 3, f"Expected (success, message, bank_identifier), got {result}"
    
    success, message, _ = result
    assert not success, "Should not be able to create account with duplicate bank identifier"
    assert "already exists" in message.lower(), f"Unexpected error message: {message}"

    # Create a different account
    different_name = f"Different Account {uuid.uuid4().hex[:8]}"
    different_identifier = f"bank_{uuid.uuid4().hex[:8]}"
    result = create_account(different_name, "Checking", "Another Bank", different_identifier)
    assert isinstance(result, tuple) and len(result) == 3, f"Expected (success, message, bank_identifier), got {result}"
    
    success, message, returned_bank_identifier = result
    assert success, f"Failed to create different account: {message}"
    assert returned_bank_identifier == different_identifier, f"Bank identifier mismatch: expected {different_identifier}, got {returned_bank_identifier}"

def test_database_connection_error(monkeypatch):
    def mock_get_transactions():
        raise DatabaseConnectionError("Database connection error")
    
    monkeypatch.setattr('services.data_service.get_transactions', mock_get_transactions)
    
    with pytest.raises(DatabaseConnectionError):
        load_transactions()
