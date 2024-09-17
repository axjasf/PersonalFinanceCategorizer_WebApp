import streamlit as st
import pandas as pd
from database.db_utils import get_session
from sqlalchemy import text

def load_accounts():
    session = get_session()
    query = text("SELECT * FROM accounts")
    result = pd.read_sql(query, session.bind)
    return result

def add_account(name, account_type, institution):
    session = get_session()
    query = text("INSERT INTO accounts (name, type, institution) VALUES (:name, :type, :institution)")
    session.execute(query, {"name": name, "type": account_type, "institution": institution})
    session.commit()

def update_account(account_id, name, account_type, institution):
    session = get_session()
    query = text("UPDATE accounts SET name = :name, type = :type, institution = :institution WHERE id = :id")
    session.execute(query, {"id": account_id, "name": name, "type": account_type, "institution": institution})
    session.commit()

def delete_account(account_id):
    session = get_session()
    query = text("DELETE FROM accounts WHERE id = :id")
    session.execute(query, {"id": account_id})
    session.commit()

st.subheader("Account Management")

# Load existing accounts
accounts = load_accounts()

# Display existing accounts
st.write("### Existing Accounts")
st.dataframe(accounts)

# Add new account
st.write("### Add New Account")
new_name = st.text_input("Account Name")
new_type = st.selectbox("Account Type", ["Bank Account", "Credit Card", "Investment", "Other"])
new_institution = st.text_input("Financial Institution")
if st.button("Add Account"):
    add_account(new_name, new_type, new_institution)
    st.success("Account added successfully!")
    st.experimental_rerun()

# Edit account
st.write("### Edit Account")
edit_account_id = st.selectbox("Select Account to Edit", accounts['id'].tolist())
edit_account = accounts[accounts['id'] == edit_account_id].iloc[0]
edit_name = st.text_input("Account Name", value=edit_account['name'])
edit_type = st.selectbox("Account Type", ["Bank Account", "Credit Card", "Investment", "Other"], index=["Bank Account", "Credit Card", "Investment", "Other"].index(edit_account['type']))
edit_institution = st.text_input("Financial Institution", value=edit_account['institution'])
if st.button("Update Account"):
    update_account(edit_account_id, edit_name, edit_type, edit_institution)
    st.success("Account updated successfully!")
    st.experimental_rerun()

# Delete account
st.write("### Delete Account")
delete_account_id = st.selectbox("Select Account to Delete", accounts['id'].tolist())
if st.button("Delete Account"):
    delete_account(delete_account_id)
    st.success("Account deleted successfully!")
    st.experimental_rerun()

st.warning("Note: Deleting an account will also delete all associated transactions and splits. This action cannot be undone.")