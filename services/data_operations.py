from database.db_utils import get_session
import pandas as pd
from sqlalchemy import text
import streamlit as st
import numpy as np

def get_transactions():
    session = get_session()
    query = text("SELECT * FROM transactions")
    st.write("Debug: Executing transactions query")
    result = pd.read_sql(query, session.bind)
    st.write(f"Debug: Retrieved {len(result)} transactions")
    return result

def get_transaction_splits(transaction_id):
    session = get_session()
    
    # Convert numpy.int64 to standard Python int
    transaction_id = int(transaction_id)
    
    # Debug: Check all splits in the database
    debug_query = text("SELECT * FROM transaction_splits")
    debug_result = pd.read_sql(debug_query, session.bind)
    st.write(f"Debug: All splits in database: {debug_result.to_dict('records')}")
    
    # Debug: Print the transaction_id and its type
    st.write(f"Debug: transaction_id: {transaction_id}, type: {type(transaction_id)}")
    
    query = text("""
        SELECT ts.*
        FROM transaction_splits ts
        WHERE ts.transaction_id = :transaction_id
    """)
    st.write(f"Debug: Executing splits query for transaction {transaction_id}")
    try:
        result = pd.read_sql(query, session.bind, params={'transaction_id': transaction_id})
        st.write(f"Debug: Retrieved {len(result)} splits")
        st.write(f"Debug: Splits data: {result.to_dict('records')}")
        
        # Debug: Execute a raw SQL query to double-check
        raw_query = f"SELECT * FROM transaction_splits WHERE transaction_id = {transaction_id}"
        raw_result = pd.read_sql(raw_query, session.bind)
        st.write(f"Debug: Raw query result: {raw_result.to_dict('records')}")
        
        return result
    except Exception as e:
        st.write(f"Error retrieving splits: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
