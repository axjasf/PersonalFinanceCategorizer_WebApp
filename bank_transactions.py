import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None
    return df

def main():
    st.title("Personal Finance Tracker")

    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            st.subheader("Raw Data")
            st.write(df)

            st.subheader("Data Summary")
            st.write(df.describe())

            # Assuming 'Amount' and 'Date' columns exist
            if 'Amount' in df.columns and 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                
                st.subheader("Transactions Over Time")
                fig = px.line(df, x='Date', y='Amount', title='Transaction Amount Over Time')
                st.plotly_chart(fig)

                st.subheader("Total Spending by Category")
                if 'Category' in df.columns:
                    category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
                    fig = px.bar(category_totals, x=category_totals.index, y='Amount', title='Total Spending by Category')
                    st.plotly_chart(fig)
                else:
                    st.write("No 'Category' column found in the data.")

if __name__ == "__main__":
    main()