import streamlit as st
import pandas as pd
from data.data_loader import load_transactions, save_transactions

def main():
    st.title("Personal Finance Tracker")

    transactions = load_transactions()
    df = pd.DataFrame(transactions)

    st.subheader("Current Transactions")
    st.dataframe(df)

    st.subheader("Add New Transaction")
    with st.form("new_transaction", clear_on_submit=True):
        date = st.date_input("Date")
        description = st.text_input("Description")
        amount = st.number_input("Amount", step=0.01)
        category = st.selectbox("Category", ["Income", "Food", "Transport", "Utilities", "Other"])

        submitted = st.form_submit_button("Add Transaction")
        if submitted:
            new_transaction = {
                "Date": date.strftime("%Y-%m-%d"),
                "Description": description,
                "Amount": amount,
                "Category": category
            }
            transactions.append(new_transaction)
            save_transactions(transactions)
            st.success("Transaction added successfully!")
            st.experimental_rerun()

    if st.button("Refresh Data"):
        st.experimental_rerun()

    # Basic analytics
    if not df.empty:
        st.subheader("Quick Analytics")
        total_income = df[df['Amount'] > 0]['Amount'].sum()
        total_expenses = df[df['Amount'] < 0]['Amount'].sum()
        st.write(f"Total Income: ${total_income:.2f}")
        st.write(f"Total Expenses: ${abs(total_expenses):.2f}")
        st.write(f"Net: ${(total_income + total_expenses):.2f}")

if __name__ == "__main__":
    main()