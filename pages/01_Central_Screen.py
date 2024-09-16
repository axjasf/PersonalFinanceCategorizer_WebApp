# ui/central_screen.py
import streamlit as st
import pandas as pd
from services.data_service import load_transactions, load_splits
from utils.ui_utils import render_aggrid
from utils.state_utils import get_grid_key, increment_grid_key
from st_aggrid import GridUpdateMode, AgGridTheme

st.set_page_config(page_title="Central Screen", layout="wide")

st.title("Central Screen: Transactions Overview")

# Render Transactions Table
transactions = load_transactions()
st.write(f"Debug: Retrieved {len(transactions)} transactions")
st.write("Debug: All transactions:", transactions.to_dict('records'))

if not transactions.empty:
    st.write("### All Transactions")
    grid_key = get_grid_key('transaction_grid_key')
    
    grid_response = render_aggrid(
        transactions,
        f'transactions_grid_{grid_key}',
        400,
        selection_mode='single',
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme=AgGridTheme.STREAMLIT
    )
    
    st.write("Debug: Grid Response Keys:", grid_response.keys())
    
    selected_rows = grid_response['selected_rows']
    st.write("Debug: Selected Rows:", selected_rows)
    st.write("Debug: Type of Selected Rows:", type(selected_rows))
    
    if st.button("Refresh Transactions"):
        increment_grid_key('transaction_grid_key')
        st.experimental_rerun()
else:
    st.write("No transactions found in the database.")

# Add a separator
st.markdown("---")

# Render Splits Table for Selected Transaction
if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
    st.write("Debug: Inside selected_rows condition")
    transaction_id = selected_rows.iloc[0]['id']
    st.write(f"Debug: Selected transaction_id: {transaction_id}")
    
    splits = load_splits(transaction_id)
    st.write(f"### Splits for Transaction ID: {transaction_id}")
    st.write(f"Debug: Splits DataFrame: {splits}")
    
    if not splits.empty:
        st.write(f"Debug: Retrieved {len(splits)} splits for the selected transaction")
        grid_key = get_grid_key('splits_grid_key')
        render_aggrid(splits, f'splits_grid_{grid_key}', 300)
    else:
        st.write("No splits found for the selected transaction.")
        st.write("Debug: Splits DataFrame is empty")
else:
    st.write("Select a transaction to view its splits.")
    st.write("Debug: selected_rows is empty or None")

