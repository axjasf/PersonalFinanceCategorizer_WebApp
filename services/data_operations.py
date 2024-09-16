from database.db_utils import get_session
import pandas as pd
from sqlalchemy import text

def get_transactions():
    session = get_session()
    query = text("SELECT * FROM transactions")
    result = pd.read_sql(query, session.bind)
    return result

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
