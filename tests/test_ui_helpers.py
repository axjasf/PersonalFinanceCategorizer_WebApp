import pytest
from utils.ui_helpers import suggest_bank_identifier

def test_suggest_bank_identifier():
    institution = "Chase"
    account_type = "Checking"
    suggested_identifier = suggest_bank_identifier(institution, account_type)
    
    assert suggested_identifier == "chase_checking"