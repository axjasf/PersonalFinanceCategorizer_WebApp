import streamlit as st
import json
from services.import_service import process_bank_file, insert_transactions, DatabaseError
from services.data_service import load_accounts
from utils.ui_helpers import render_grid

IMPORT_TRANSACTIONS_TITLE = "Import Transactions"

st.set_page_config(page_title=IMPORT_TRANSACTIONS_TITLE, page_icon="📥", layout="wide")

st.title(IMPORT_TRANSACTIONS_TITLE)

# Load field mappings
with open('config/field_mappings.json') as f:
    field_mappings = json.load(f)

# Load accounts and create a selection box
accounts = load_accounts()
selected_account = st.selectbox("Select Account", options=accounts['name'].tolist())

# File uploader for transactions
uploaded_file = st.file_uploader("Choose a CSV file for transactions", type="csv")

# Get bank identifier
bank_identifier = accounts[accounts['name'] == selected_account]['bank_identifier'].iloc[0]

# Check if currency conversion is needed
needs_currency_conversion = field_mappings[bank_identifier].get('needs_currency_conversion', False)

# File uploader for exchange rates if needed
exchange_rates_file = None
if needs_currency_conversion:
    exchange_rates_file = st.file_uploader("Upload Exchange Rates CSV", type="csv")

if uploaded_file is not None:
    try:
        # Process the import
        mapped_df = process_bank_file(bank_identifier, uploaded_file, exchange_rates_file, field_mappings)
        
        # Get mapped columns
        mapped_columns = list(field_mappings[bank_identifier]['fields'].keys())
        if 'payee' in mapped_columns:
            mapped_columns.remove('payee')
            mapped_columns.append('payee_id')
        
        # Display the raw CSV data in an AgGrid
        st.write("### Raw CSV Data:")
        render_grid(mapped_df, {}, 'raw_csv', 400)
        
        # Display only mapped columns in the mapped data preview
        st.write("### Mapped Data Preview:")
        mapped_preview_df = mapped_df[mapped_columns]
        render_grid(mapped_preview_df, {}, 'mapped_data', 400)
        
        # Import button
        if st.button(IMPORT_TRANSACTIONS_TITLE):
            try:
                success = insert_transactions(mapped_preview_df)
                if success:
                    st.success("Transactions imported successfully!")
            except DatabaseError as e:
                st.error(f"Failed to import transactions: {str(e)}")
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
