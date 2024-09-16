# ui/central_screen.py
import streamlit as st
from services.data_service import load_transactions, load_splits
from utils.ui_utils import render_aggrid
from utils.state_utils import get_grid_key, increment_grid_key

st.set_page_config(page_title="Central Screen", layout="wide")

st.title("Central Screen: Transactions Overview")

# Render Transactions Table
transactions = load_transactions()
st.write(f"Debug: Retrieved {len(transactions)} transactions")

if not transactions.empty:
    st.write("### All Transactions")
    grid_key = get_grid_key('transaction_grid_key')
    render_aggrid(transactions, f'transactions_grid_{grid_key}', 400)
    if st.button("Refresh Transactions"):
        increment_grid_key('transaction_grid_key')
        st.experimental_rerun()
else:
    st.write("No transactions found in the database.")

# Add a separator
st.markdown("---")

# Render Splits Table
splits = load_splits()
st.write(f"Debug: Retrieved {len(splits)} splits")

if not splits.empty:
    st.write("### All Splits")
    st.write("This table shows all split transactions across all transactions.")
    grid_key = get_grid_key('splits_grid_key')
    render_aggrid(splits, f'splits_grid_{grid_key}', 300)
    if st.button("Refresh Splits"):
        increment_grid_key('splits_grid_key')
        st.experimental_rerun()
else:
    st.write("No splits found in the database.")

