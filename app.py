# app.py
import streamlit as st
from database.db_utils import init_db
from ui import (
    central_screen,
    import_transactions_screen,
    upload_orders_screen,
    payee_management_screen,
    account_management_screen,
    tagging_notes_screen,
    reconciliation_tools_screen
)

# Initialize the database
init_db()

# App title
st.title("Personal Finance Transaction Categorization System")

# Navigation Menu
menu = [
    "Central Screen",
    "Import Transactions",
    "Upload Orders",
    "Payee Management",
    "Account Management",
    "Tagging & Notes",
    "Reconciliation Tools"
]
choice = st.sidebar.selectbox("Menu", menu)

# Render the selected screen
if choice == "Central Screen":
    central_screen.render()
elif choice == "Import Transactions":
    import_transactions_screen.render()
elif choice == "Upload Orders":
    upload_orders_screen.render()
elif choice == "Payee Management":
    payee_management_screen.render()
elif choice == "Account Management":
    account_management_screen.render()
elif choice == "Tagging & Notes":
    tagging_notes_screen.render()
elif choice == "Reconciliation Tools":
    reconciliation_tools_screen.render()
