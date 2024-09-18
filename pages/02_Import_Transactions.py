import streamlit as st
import json
from services.import_service import process_import, insert_transactions, DatabaseError
from services.data_service import load_accounts
from utils.ui_helpers import render_grid

st.set_page_config(page_title="Import Transactions", page_icon="📥", layout="wide")

st.title("Import Transactions")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Load field mappings
        with open('config/field_mappings.json') as f:
            field_mappings = json.load(f)
        
        # Load accounts and create a selection box
        accounts = load_accounts()
        selected_account = st.selectbox("Select Account", options=accounts['name'].tolist())
        
        # Process the import
        mapped_df, validation_errors = process_import(uploaded_file, selected_account, field_mappings)
        
        # Display the raw CSV data in an AgGrid
        st.write("### Raw CSV Data:")
        render_grid(mapped_df, {}, 'raw_csv', 400)
        
        # Display the mapped DataFrame in an AgGrid
        st.write("### Mapped Data Preview:")
        render_grid(mapped_df, {}, 'mapped_data', 400)
        
        if validation_errors:
            st.error("Validation Errors:")
            for error in validation_errors:
                st.write(error)
        else:
            # Import button
            if st.button("Import Transactions"):
                try:
                    success = insert_transactions(mapped_df)
                    if success:
                        st.success("Transactions imported successfully!")
                except DatabaseError as e:
                    st.error(f"Failed to import transactions: {str(e)}")
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
