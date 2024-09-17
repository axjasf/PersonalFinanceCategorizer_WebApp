import pytest
import pandas as pd
from utils.ui_helpers import render_transactions_grid, render_splits_grid

@pytest.fixture
def sample_transactions_data():
    return pd.DataFrame({
        'Id': [1, 2],
        'Date': ['2023-01-01', '2023-01-02'],
        'Amount': [100.0, 200.0],
        'Description': ['Test 1', 'Test 2']
    })

@pytest.fixture
def sample_splits_data():
    return pd.DataFrame({
        'Id': [1, 2],
        'Category': ['Food', 'Transport'],
        'Amount': [50.0, 50.0]
    })

def test_render_transactions_grid(sample_transactions_data):
    grid_response = render_transactions_grid(sample_transactions_data)
    assert 'data' in grid_response
    assert len(grid_response['data']) == 2
    assert 'columnDefs' in grid_response
    assert len(grid_response['columnDefs']) == 4

def test_render_splits_grid(sample_splits_data):
    grid_response = render_splits_grid(sample_splits_data)
    assert 'data' in grid_response
    assert len(grid_response['data']) == 2
    assert 'columnDefs' in grid_response
    assert len(grid_response['columnDefs']) == 3
