"""
Data service layer for the Personal Finance Categorizer.
Provides cached data loading functions for transactions and splits,
acting as an intermediary between the UI and data operations.
"""

import streamlit as st
from .data_operations import get_transactions, get_transaction_splits, get_accounts, add_account, update_account, delete_account, AccountAlreadyExistsError

@st.cache_data(ttl=300)
def load_transactions():
    return get_transactions()

@st.cache_data(ttl=300)
def load_splits(transaction_id):
    return get_transaction_splits(int(transaction_id))

@st.cache_data(ttl=300)
def load_accounts():
    return get_accounts()

def create_account(name, account_type, institution):
    try:
        add_account(name, account_type, institution)
        st.cache_data.clear()  # Clear cache after adding an account
        return True, "Account added successfully!"
    except AccountAlreadyExistsError as e:
        return False, str(e)

def modify_account(account_id, name, account_type, institution):
    update_account(account_id, name, account_type, institution)
    st.cache_data.clear()  # Clear cache after modifying an account

def remove_account(account_id):
    delete_account(account_id)
    st.cache_data.clear()  # Clear cache after removing an account
