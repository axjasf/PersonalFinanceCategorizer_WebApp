import streamlit as st
from .data_operations import get_transactions, get_transaction_splits

@st.cache_data(ttl=300)
def load_transactions():
    return get_transactions()

@st.cache_data(ttl=300)
def load_splits(transaction_id):
    splits = get_transaction_splits(transaction_id)
    st.write(f"Debug: load_splits called for transaction_id: {transaction_id}")
    st.write(f"Debug: Splits data: {splits}")
    return splits
