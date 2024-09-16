from database.db_utils import get_session
import pandas as pd
from sqlalchemy import text

def get_transactions():
    session = get_session()
    query = text("SELECT * FROM transactions")
    return pd.read_sql(query, session.bind)

def get_all_splits():
    session = get_session()
    query = text("SELECT * FROM transaction_splits")
    return pd.read_sql(query, session.bind)
