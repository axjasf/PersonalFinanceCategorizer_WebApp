import pytest
from database.db_utils import init_db, get_session
from sqlalchemy import text

def test_database_initialization():
    init_db()
    session = get_session()
    
    # Test if tables are created
    tables = ['accounts', 'categories', 'payees', 'transactions', 'transaction_splits']
    for table in tables:
        result = session.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"))
        assert result.fetchone() is not None, f"Table {table} was not created"

    # Test if accounts table has correct columns
    result = session.execute(text("PRAGMA table_info(accounts)"))
    columns = [row['name'] for row in result.fetchall()]
    expected_columns = ['id', 'name', 'type', 'institution']
    for col in expected_columns:
        assert col in columns, f"Column {col} is missing in accounts table"
