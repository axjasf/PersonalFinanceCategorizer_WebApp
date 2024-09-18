"""
Data service layer for the Personal Finance Categorizer.
Provides cached data loading functions for transactions, splits, and accounts,
acting as an intermediary between the UI and data operations.
"""

import streamlit as st
from .data_operations import get_transactions, get_transaction_splits, get_accounts, add_account, update_account, delete_account, AccountAlreadyExistsError

def suggest_bank_identifier(institution, account_type):
    return f"{institution.lower().replace(' ', '_')}_{account_type.lower()}"

@st.cache_data(ttl=300)
def load_transactions():
    return get_transactions()

@st.cache_data(ttl=300)
def load_splits(transaction_id):
    return get_transaction_splits(int(transaction_id))

@st.cache_data(ttl=300)
def load_accounts():
    return get_accounts()

def create_account(name, account_type, institution, bank_identifier=None):
    if bank_identifier is None:
        bank_identifier = suggest_bank_identifier(institution, account_type)
    try:
        account_id = add_account(name, account_type, institution, bank_identifier)
        st.cache_data.clear()  # Clear cache after adding an account
        return True, f"Account added successfully with ID: {account_id}", bank_identifier
    except AccountAlreadyExistsError as e:
        return False, str(e), bank_identifier

def modify_account(account_id, name, account_type, institution, bank_identifier):
    try:
        update_account(account_id, name, account_type, institution, bank_identifier)
        st.cache_data.clear()  # Clear cache after modifying an account
        return True, "Account updated successfully", bank_identifier
    except Exception as e:
        return False, f"Failed to update account: {str(e)}", bank_identifier

def remove_account(account_id):
    try:
        delete_account(account_id)
        st.cache_data.clear()  # Clear cache after deleting an account
        return True, "Account deleted successfully"
    except Exception as e:
        return False, f"Failed to delete account: {str(e)}"

def handle_bank_identifier_suggestion(institution, account_type, prev_institution, prev_type, prev_suggested_identifier):
    if prev_institution != institution or prev_type != account_type:
        suggested_identifier = suggest_bank_identifier(institution, account_type)
    else:
        suggested_identifier = prev_suggested_identifier
    return suggested_identifier, institution, account_type
