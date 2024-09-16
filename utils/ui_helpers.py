from utils.ui_utils import render_aggrid
from utils.state_utils import get_grid_key
from st_aggrid import GridUpdateMode, AgGridTheme

def render_transactions_grid(transactions):
    grid_key = get_grid_key('transaction_grid_key')
    return render_aggrid(
        transactions,
        f'transactions_grid_{grid_key}',
        400,
        selection_mode='single',
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme=AgGridTheme.STREAMLIT
    )

def render_splits_grid(splits):
    grid_key = get_grid_key('splits_grid_key')
    return render_aggrid(splits, f'splits_grid_{grid_key}', 300)
