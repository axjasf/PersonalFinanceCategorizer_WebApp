"""
Core data operations for the Personal Finance Categorizer.
Contains functions for retrieving transactions and splits from the database,
using SQLAlchemy queries and returning pandas DataFrames.
"""

from database.db_utils import get_session
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class AccountAlreadyExistsError(Exception):
    pass

class DatabaseConnectionError(Exception):
    """Raised when there's an issue connecting to the database."""
    pass

def get_transactions():
    try:
        session = get_session()
        query = text("SELECT * FROM vw_transactions_with_details")
        result = pd.read_sql(query, session.bind)
        return result
    except SQLAlchemyError as e:
        raise DatabaseConnectionError(f"Failed to retrieve transactions: {str(e)}") from e

def get_transaction_splits(transaction_id):
    session = get_session()
    transaction_id = int(transaction_id)  # Convert to standard Python int
    query = text("""
        SELECT ts.*, c.name as category_name
        FROM transaction_splits ts
        JOIN categories c ON ts.category_id = c.id
        WHERE ts.transaction_id = :transaction_id
    """)
    result = pd.read_sql(query, session.bind, params={'transaction_id': transaction_id})
    return result

def get_accounts():
    session = get_session()
    query = text("SELECT * FROM accounts")
    result = pd.read_sql(query, session.bind)
    return result

def add_account(name, account_type, institution, bank_identifier):
    session = get_session()
    query = text("INSERT INTO accounts (name, type, institution, bank_identifier) VALUES (:name, :type, :institution, :bank_identifier)")
    try:
        result = session.execute(query, {
            "name": name, 
            "type": account_type, 
            "institution": institution,
            "bank_identifier": bank_identifier
        })
        session.commit()
        return result.lastrowid  # or some other indication of success
    except IntegrityError:
        session.rollback()
        raise AccountAlreadyExistsError(f"An account with the name '{name}' or bank identifier '{bank_identifier}' already exists.")

def update_account(account_id, name, account_type, institution):
    session = get_session()
    query = text("UPDATE accounts SET name = :name, type = :type, institution = :institution WHERE id = :id")
    session.execute(query, {"id": account_id, "name": name, "type": account_type, "institution": institution})
    session.commit()

def delete_account(account_id):
    session = get_session()
    query = text("DELETE FROM accounts WHERE id = :id")
    session.execute(query, {"id": account_id})
    session.commit()
