import pytest
from config import DATABASE_URI, ACCOUNT_TYPES

def test_database_uri_configuration():
    assert DATABASE_URI.startswith('sqlite:///')

def test_account_types_configuration():
    assert isinstance(ACCOUNT_TYPES, list)
    assert len(ACCOUNT_TYPES) > 0
    assert 'Checking' in ACCOUNT_TYPES
    assert 'Savings' in ACCOUNT_TYPES
