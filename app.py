import streamlit as st
from data.data_loader import load_transactions
from ui.dashboard import display_dashboard

def main():
    st.title("Personal Finance Categorizer")
    st.write("Welcome to the Personal Finance Categorizer Web App!")

    transactions = load_transactions()
    display_dashboard(transactions)

if __name__ == "__main__":
    main()