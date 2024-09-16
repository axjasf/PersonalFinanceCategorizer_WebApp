# ui/central_screen.py
import streamlit as st
import pandas as pd
from services.data_service import load_transactions, load_splits
from utils.ui_helpers import render_transactions_grid, render_splits_grid

st.set_page_config(page_title="Central Screen", layout="wide")

st.title("Central Screen: Transactions Overview")

# Render Transactions Table
transactions = load_transactions()

if not transactions.empty:
    st.write("### All Transactions")
    grid_response = render_transactions_grid(transactions)
    
    selected_rows = grid_response['selected_rows']
else:
    st.write("No transactions found in the database.")

# Add a separator
st.markdown("---")

# Render Splits Table for Selected Transaction
if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
    transaction_id = selected_rows.iloc[0]['id']
    
    splits = load_splits(transaction_id)
    st.write(f"### Splits for Transaction ID: {transaction_id}")
    
    if not splits.empty:
        render_splits_grid(splits)
    else:
        st.write("No splits found for the selected transaction.")
else:
    st.write("Select a transaction to view its splits.")

