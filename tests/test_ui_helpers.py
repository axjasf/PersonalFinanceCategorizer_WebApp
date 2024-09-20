import pytest
import pandas as pd
from utils.ui_helpers import (
    prettify_column_names,
    format_currency,
    render_grid,
    render_transactions_grid,
    render_splits_grid,
    render_accounts_grid,
    suggest_bank_identifier
)
import streamlit as st
from unittest.mock import MagicMock

class TestUIHelpers:

    @pytest.fixture(autouse=True)
    def mock_streamlit(self, mocker):
        mocker.patch.object(st, 'session_state', new_callable=MagicMock)

    @pytest.fixture
    def sample_dataframe(self):
        return pd.DataFrame({
            'id': [1, 2, 3],
            'transaction_date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'amount': [100.50, 200.75, 300.25],
            'payee_name': ['Store A', 'Store B', 'Store C'],
            'account_name': ['Checking', 'Savings', 'Credit Card'],
            'description': ['Purchase 1', 'Purchase 2', 'Purchase 3']
        })

    def test_prettify_column_names(self, sample_dataframe):
        result = prettify_column_names(sample_dataframe)
        assert 'Transaction Date' in result.columns
        assert 'Payee Name' in result.columns

    def test_format_currency(self):
        assert format_currency(100.50) == "$100.50"
        assert format_currency(1000.75) == "$1,000.75"

    def test_render_grid(self, sample_dataframe, mocker):
        mocker.patch('utils.ui_helpers.render_aggrid', return_value={})
        mocker.patch('utils.state_utils.get_grid_key', return_value=0)
        result = render_grid(sample_dataframe, {}, 'test', 400)
        assert isinstance(result, dict)

    def test_render_transactions_grid(self, sample_dataframe, mocker):
        mocker.patch('utils.ui_helpers.render_grid', return_value={})
        result = render_transactions_grid(sample_dataframe)
        assert isinstance(result, dict)

    def test_render_splits_grid(self, mocker):
        splits_df = pd.DataFrame({
            'id': [1, 2],
            'category_name': ['Food', 'Transport'],
            'allocated_amount': [50.25, 30.75]
        })
        mocker.patch('utils.ui_helpers.render_grid', return_value={})
        result = render_splits_grid(splits_df)
        assert isinstance(result, dict)

    def test_suggest_bank_identifier(self):
        result = suggest_bank_identifier("Chase", "Checking")
        assert result == "chase_checking"