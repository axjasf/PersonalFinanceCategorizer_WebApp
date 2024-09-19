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

class TestTransactions:
    def test_get_transactions(self, setup_database):
        transactions = get_transactions()
        assert isinstance(transactions, pd.DataFrame)
        assert 'id' in transactions.columns
        assert 'transaction_date' in transactions.columns

    def test_get_transaction_splits(self, setup_database):
        # First, add a transaction and a split
        session = get_session()
        session.execute(text("INSERT INTO transactions (transaction_date, amount, description) VALUES ('2023-01-01', 100.0, 'Test Transaction')"))
        session.execute(text("INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount) VALUES (1, 1, 100.0)"))
        session.commit()

        splits = get_transaction_splits(1)
        assert isinstance(splits, pd.DataFrame)
        assert 'id' in splits.columns
        assert 'allocated_amount' in splits.columns

class TestAccounts:
    def test_get_accounts(self, setup_database):
        accounts = get_accounts()
        assert isinstance(accounts, pd.DataFrame)
        assert 'id' in accounts.columns
        assert 'name' in accounts.columns

    def test_add_account(self, setup_database):
        # Generate a unique account name and bank identifier
        unique_name = f"Test Account {uuid.uuid4().hex[:8]}"
        unique_identifier = f"bank_{uuid.uuid4().hex[:8]}"
        
        # Test successful account addition
        result = add_account(unique_name, "Checking", "Test Bank", unique_identifier)
        assert result is not None, "Account should be added successfully"
        
        # Test adding an account with the same name (should raise an error)
        with pytest.raises(AccountAlreadyExistsError):
            add_account(unique_name, "Savings", "Another Bank", f"bank_{uuid.uuid4().hex[:8]}")

        # Test adding another unique account
        another_unique_name = f"Another Account {uuid.uuid4().hex[:8]}"
        another_unique_identifier = f"bank_{uuid.uuid4().hex[:8]}"
        another_result = add_account(another_unique_name, "Savings", "Another Bank", another_unique_identifier)
        assert another_result is not None, "Second unique account should be added successfully"

    def test_add_duplicate_account(self, setup_database):
        # Generate a unique account name and bank identifier
        unique_name = f"Unique Account {uuid.uuid4().hex[:8]}"
        unique_identifier = f"bank_{uuid.uuid4().hex[:8]}"
        
        # Add an account
        add_account(unique_name, "Savings", "Another Bank", unique_identifier)
        
        # Try to add the same account again
        with pytest.raises(AccountAlreadyExistsError, match=f"An account with the name '{unique_name}' or bank identifier '{unique_identifier}' already exists"):
            add_account(unique_name, "Savings", "Another Bank", unique_identifier)

        # Try to add an account with the same name but different bank identifier
        with pytest.raises(AccountAlreadyExistsError, match=f"An account with the name '{unique_name}' or bank identifier '.*' already exists"):
            add_account(unique_name, "Savings", "Another Bank", f"bank_{uuid.uuid4().hex[:8]}")

        # Try to add an account with a different name but same bank identifier
        with pytest.raises(AccountAlreadyExistsError, match=f"An account with the name '.*' or bank identifier '{unique_identifier}' already exists"):
            add_account(f"Different Account {uuid.uuid4().hex[:8]}", "Savings", "Another Bank", unique_identifier)

    def test_update_account(self, setup_database):
        # First, add two accounts
        unique_name1 = f"Test Account {uuid.uuid4().hex[:8]}"
        unique_identifier1 = f"bank_{uuid.uuid4().hex[:8]}"
        account_id1 = add_account(unique_name1, "Checking", "Test Bank", unique_identifier1)

        unique_name2 = f"Test Account {uuid.uuid4().hex[:8]}"
        unique_identifier2 = f"bank_{uuid.uuid4().hex[:8]}"
        account_id2 = add_account(unique_name2, "Savings", "Another Bank", unique_identifier2)
        
        # Update the first account
        new_name = f"Updated Account {uuid.uuid4().hex[:8]}"
        new_type = "Savings"
        new_institution = "New Bank"
        new_identifier = f"bank_{uuid.uuid4().hex[:8]}"
        
        update_account(account_id1, new_name, new_type, new_institution, new_identifier)
        
        # Verify the update
        accounts = get_accounts()
        updated_account = accounts[accounts['id'] == account_id1].iloc[0]
        assert updated_account['name'] == new_name
        assert updated_account['type'] == new_type
        assert updated_account['institution'] == new_institution
        assert updated_account['bank_identifier'] == new_identifier

        # Test updating with an existing name
        with pytest.raises(AccountAlreadyExistsError):
            update_account(account_id1, unique_name2, new_type, new_institution, new_identifier)

        # Test updating with an existing identifier
        with pytest.raises(AccountAlreadyExistsError):
            update_account(account_id1, new_name, new_type, new_institution, unique_identifier2)

        # Test updating a non-existent account
        non_existent_id = max(account_id1, account_id2) + 1  # An ID that doesn't exist
        with pytest.raises(ValueError, match=f"No account found with id: {non_existent_id}"):
            update_account(non_existent_id, "New Name", "Checking", "New Bank", "new_identifier")

    def test_delete_account(self, setup_database):
        # First, add an account
        unique_name = f"Test Account {uuid.uuid4().hex[:8]}"
        unique_identifier = f"bank_{uuid.uuid4().hex[:8]}"
        account_id = add_account(unique_name, "Checking", "Test Bank", unique_identifier)
        
        # Delete the account
        delete_account(account_id)
        
        # Verify the deletion
        accounts = get_accounts()
        assert account_id not in accounts['id'].values

        # Test deleting a non-existent account
        with pytest.raises(ValueError):
            delete_account(account_id)
