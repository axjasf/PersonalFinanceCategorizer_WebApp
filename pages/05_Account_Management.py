# Account Management page for the Personal Finance Categorizer.
# This page allows users to view, add, edit, and delete accounts.
# It interacts with the data service layer to perform CRUD operations on accounts.

import streamlit as st
from services.data_service import load_accounts, create_account, modify_account, remove_account, suggest_bank_identifier
from utils.ui_helpers import render_accounts_grid
from config import ACCOUNT_TYPES

st.set_page_config(page_title="Account Management", layout="wide")

st.title("Account Management")

# Load existing accounts
accounts = load_accounts()

# Display existing accounts
st.write("### Existing Accounts")
grid_response = render_accounts_grid(accounts)

# Add new account
st.write("### Add New Account")
new_name = st.text_input("Account Name", key="new_account_name")
new_type = st.selectbox("Account Type", ACCOUNT_TYPES, key="new_account_type")
new_institution = st.text_input("Financial Institution", key="new_account_institution")

# Suggest bank identifier when institution or account type changes
suggested_identifier, st.session_state['prev_institution'], st.session_state['prev_type'] = handle_bank_identifier_suggestion(
    new_institution,
    new_type,
    st.session_state.get('prev_institution'),
    st.session_state.get('prev_type'),
    st.session_state.get('suggested_identifier', '')
)

new_bank_identifier = st.text_input("Bank Identifier", 
                                    value=suggested_identifier,
                                    key="new_account_bank_identifier")
st.session_state['suggested_identifier'] = new_bank_identifier

if st.button("Add Account"):
    success, message, _ = create_account(new_name, new_type, new_institution)
    if success:
        st.success(message)
        st.rerun()
    else:
        st.error(message)

# Edit account
st.write("### Edit Account")
if not accounts.empty:
    edit_account_id = st.selectbox("Select Account to Edit", accounts['id'].tolist(), key="edit_account_select")
    edit_account = accounts[accounts['id'] == edit_account_id].iloc[0]
    edit_name = st.text_input("Account Name", value=edit_account['name'], key="edit_account_name")
    edit_type = st.selectbox("Account Type", ACCOUNT_TYPES, 
                             index=ACCOUNT_TYPES.index(edit_account['type']),
                             key="edit_account_type")
    edit_institution = st.text_input("Financial Institution", value=edit_account['institution'], key="edit_account_institution")
    
    if st.button("Update Account"):
        success, message, _ = modify_account(edit_account_id, edit_name, edit_type, edit_institution)
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)
else:
    st.write("No accounts available to edit.")

# Delete account
st.write("### Delete Account")
if not accounts.empty:
    delete_account_id = st.selectbox("Select Account to Delete", accounts['id'].tolist(), key="delete_account_select")
    if st.button("Delete Account"):
        success, message = remove_account(delete_account_id)
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)
else:
    st.write("No accounts available to delete.")

st.warning("Note: Deleting an account will also delete all associated transactions and splits. This action cannot be undone.")