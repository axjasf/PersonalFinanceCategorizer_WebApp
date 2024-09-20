import pytest
from database.db_utils import init_db, get_session
from sqlalchemy import text


@pytest.fixture(scope="module")
def db_session():
    init_db()
    session = get_session()
    yield session
    session.close()


@pytest.mark.database
def test_database_initialization(db_session):
    # Test if tables are created
    tables = ["accounts", "categories", "payees", "transactions", "transaction_splits"]
    for table in tables:
        result = db_session.execute(
            text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        )
        assert result.scalar() is not None, f"Table {table} was not created"

    # Test if views are created
    views = ["vw_transactions_with_details"]  # Add all your view names here
    for view in views:
        result = db_session.execute(
            text(f"SELECT name FROM sqlite_master WHERE type='view' AND name='{view}'")
        )
        assert result.scalar() is not None, f"View {view} was not created"

    # Test if accounts table has correct columns
    result = db_session.execute(text("PRAGMA table_info(accounts)"))
    columns = [row[1] for row in result.fetchall()]  # column name is at index 1
    expected_columns = ["id", "name", "type", "institution", "bank_identifier"]
    for col in expected_columns:
        assert (
            col in columns
        ), f"Column {col} is missing in accounts table. Found columns: {columns}"

    print("Database initialization test passed successfully.")


@pytest.mark.database
def test_invalid_query(db_session):
    with pytest.raises(Exception):
        db_session.execute(text("SELECT * FROM non_existent_table"))
