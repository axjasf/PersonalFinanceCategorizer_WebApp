# ui/central_screen.py
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, AgGridTheme
from services.data_operations import get_transactions, get_all_splits
import pandas as pd

st.title("Transactions Overview")

def render_aggrid(dataframe: pd.DataFrame, key: str, height: int):
    gb = GridOptionsBuilder.from_dataframe(dataframe)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gridOptions = gb.build()
    
    AgGrid(
        dataframe,
        gridOptions=gridOptions,
        enable_enterprise_modules=False,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme=AgGridTheme.STREAMLIT,
        height=height,
        fit_columns_on_grid_load=True,
        key=key
    )


# Render Transactions Table
transactions = get_transactions()
st.write("Debug: Transactions DataFrame")
st.write(transactions)

if not transactions.empty:
    st.write("### All Transactions")
    render_aggrid(transactions, 'transactions_grid', 400)
else:
    st.write("No transactions found in the database.")

# Add a separator
st.markdown("---")

# Render Splits Table
splits = get_all_splits()
st.write("Debug: Splits DataFrame")
st.write(splits)
    
if not splits.empty:
    st.write("### All Splits")
    st.write("This table shows all split transactions across all transactions.")
    render_aggrid(splits, 'splits_grid', 300)
else:
    st.write("No splits found in the database.")

