# ui/central_screen.py
import streamlit as st
from services.data_operations import get_transactions, get_all_splits
from utils.ui_utils import render_aggrid

st.title("Central Screen: Transactions Overview")

# Render Transactions Table
transactions = get_transactions()

if not transactions.empty:
    st.write("### All Transactions")
    render_aggrid(transactions, 'transactions_grid', 400)
else:
    st.write("No transactions found in the database.")

# Add a separator
st.markdown("---")

# Render Splits Table
splits = get_all_splits()

if not splits.empty:
    st.write("### All Splits")
    st.write("This table shows all split transactions across all transactions.")
    render_aggrid(splits, 'splits_grid', 300)
else:
    st.write("No splits found in the database.")

