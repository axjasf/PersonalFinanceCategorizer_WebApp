from database.db_utils import get_session
import pandas as pd
from sqlalchemy import text
import streamlit as st

def get_transactions():
    session = get_session()
    query = text("SELECT * FROM transactions")
    st.write("Debug: Executing transactions query")
    result = pd.read_sql(query, session.bind)
    st.write(f"Debug: Retrieved {len(result)} transactions")
    return result

def get_all_splits():
    session = get_session()
    query = text("SELECT * FROM transaction_splits")
    st.write("Debug: Executing splits query")
    result = pd.read_sql(query, session.bind)
    st.write(f"Debug: Retrieved {len(result)} splits")
    return result
