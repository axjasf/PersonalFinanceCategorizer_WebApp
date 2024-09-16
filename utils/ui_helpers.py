from utils.ui_utils import render_aggrid
from utils.state_utils import get_grid_key
from st_aggrid import GridUpdateMode, AgGridTheme

def prettify_column_names(df, custom_mappings=None):
    if custom_mappings:
        df = df.rename(columns=custom_mappings)
    return df.rename(columns=lambda x: x.replace('_', ' ').title())

def format_currency(value):
    return f"${value:,.2f}"

def render_grid(data, custom_mappings, grid_key_prefix, height):
    # Prettify column names
    data = prettify_column_names(data, custom_mappings)
    
    # Ensure 'ID' remains capitalized if present
    if 'ID' in data.columns:
        data = data.rename(columns={'ID': 'ID'})
    
    # Format currency columns
    for col in data.columns:
        if 'Amount' in col:
            data[col] = data[col].apply(format_currency)
    
    grid_key = get_grid_key(f'{grid_key_prefix}_grid_key')
    return render_aggrid(
        data,
        f'{grid_key_prefix}_grid_{grid_key}',
        height,
        selection_mode='single',
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme=AgGridTheme.STREAMLIT
    )

def render_transactions_grid(transactions):
    custom_mappings = {
        'id': 'ID',
        'transaction_date': 'Date',
        'amount': 'Amount',
        'payee': 'Payee',
        'account': 'Account',
        'description': 'Description'
    }
    return render_grid(transactions, custom_mappings, 'transactions', 400)

def render_splits_grid(splits):
    custom_mappings = {
        'id': 'ID',
        'category_name': 'Category',
        'allocated_amount': 'Allocated Amount'
    }
    return render_grid(splits, custom_mappings, 'splits', 300)
