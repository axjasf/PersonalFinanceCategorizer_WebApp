"""
Data service layer for the Personal Finance Categorizer.
Provides cached data loading functions for transactions and splits,
acting as an intermediary between the UI and data operations.
"""

import streamlit as st
from .data_operations import get_transactions, get_transaction_splits

@st.cache_data(ttl=300)
def load_transactions():
    return get_transactions()

@st.cache_data(ttl=300)
def load_splits(transaction_id):
    return get_transaction_splits(int(transaction_id))
