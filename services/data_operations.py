"""
Core data operations for the Personal Finance Categorizer.
Contains functions for retrieving and modifying transactions, splits, and accounts in the database,
using SQLAlchemy queries and returning pandas DataFrames.
"""

from database.db_utils import get_session
from database.models import Account, Transaction, SplitTransaction
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class AccountAlreadyExistsError(Exception):
    pass

class DatabaseError(Exception):
    pass

def get_transactions():
    try:
        session = get_session()
        query = text("SELECT * FROM vw_transactions_with_details")
        result = pd.read_sql(query, session.bind)
        return result
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to retrieve transactions: {str(e)}")

def get_transaction_splits(transaction_id):
    try:
        session = get_session()
        query = text("""
            SELECT ts.*, c.name as category_name
            FROM transaction_splits ts
            JOIN categories c ON ts.category_id = c.id
            WHERE ts.transaction_id = :transaction_id
        """)
        result = pd.read_sql(query, session.bind, params={'transaction_id': transaction_id})
        return result
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to retrieve transaction splits: {str(e)}")

def get_accounts():
    try:
        session = get_session()
        query = text("SELECT * FROM accounts")
        result = pd.read_sql(query, session.bind)
        return result
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to retrieve accounts: {str(e)}")

def add_account(name, account_type, institution, bank_identifier):
    session = get_session()
    new_account = Account(name=name, type=account_type, institution=institution, bank_identifier=bank_identifier)
    session.add(new_account)
    try:
        session.commit()
        return new_account.id
    except IntegrityError:
        session.rollback()
        raise AccountAlreadyExistsError(f"An account with the name '{name}' or bank identifier '{bank_identifier}' already exists.")
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseError(f"Failed to add account: {str(e)}")

def update_account(account_id, name, account_type, institution, bank_identifier):
    session = get_session()
    account = session.query(Account).get(account_id)
    if not account:
        raise ValueError(f"No account found with id: {account_id}")
    account.name = name
    account.type = account_type
    account.institution = institution
    account.bank_identifier = bank_identifier
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise AccountAlreadyExistsError(f"An account with the name '{name}' or bank identifier '{bank_identifier}' already exists.")
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseError(f"Failed to update account: {str(e)}")

def delete_account(account_id):
    session = get_session()
    account = session.query(Account).get(account_id)
    if not account:
        raise ValueError(f"No account found with id: {account_id}")
    try:
        session.delete(account)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseError(f"Failed to delete account: {str(e)}")
