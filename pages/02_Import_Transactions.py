import streamlit as st
import pandas as pd
from services.import_service import read_csv, apply_field_mapping, validate_data, insert_transactions
import json
from services.data_service import load_accounts

st.set_page_config(page_title="Import Transactions", page_icon="📥")

st.title("Import Transactions")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = read_csv(uploaded_file)
    
    # Load field mappings
    with open('config/field_mappings.json') as f:
        field_mappings = json.load(f)
    
    # Select bank for field mapping
    bank = st.selectbox("Select Bank", options=list(field_mappings.keys()))
    
    # Apply field mapping
    mapped_df = apply_field_mapping(df, field_mappings[bank])
    
    # Display the mapped DataFrame
    st.write("Mapped Data Preview:")
    st.write(mapped_df.head())
    
    # Validate data
    validation_errors = validate_data(mapped_df)
    if validation_errors:
        st.error("Validation Errors:")
        for error in validation_errors:
            st.write(error)
    else:
        # Import button
        if st.button("Import Transactions"):
            success = insert_transactions(mapped_df)
            if success:
                st.success("Transactions imported successfully!")
            else:
                st.error("Failed to import transactions. Please try again.")
