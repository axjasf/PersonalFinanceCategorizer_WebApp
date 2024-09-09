import streamlit as st
from data.data_loader import load_transactions, save_transactions
from ui.dashboard import display_dashboard

def main():
    st.set_page_config(page_title="Personal Finance App", layout="wide")
    transactions = load_transactions()
    display_dashboard(transactions)

if __name__ == "__main__":
    main()