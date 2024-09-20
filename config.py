"""
Configuration file for the Personal Finance Categorizer application.
Contains global settings such as database URI and import batch size.
"""

DATABASE_URI = "sqlite:///data/personalfinance.db"
IMPORT_BATCH_SIZE = 1000

# Account Types
ACCOUNT_TYPE_CHECKING = "Checking"
ACCOUNT_TYPE_SAVINGS = "Savings"
ACCOUNT_TYPE_CREDIT = "Credit Card"
ACCOUNT_TYPE_INVESTMENT = "Investment"
ACCOUNT_TYPE_OTHER = "Other"

ACCOUNT_TYPES = [
    ACCOUNT_TYPE_CHECKING,
    ACCOUNT_TYPE_SAVINGS,
    ACCOUNT_TYPE_CREDIT,
    ACCOUNT_TYPE_INVESTMENT,
    ACCOUNT_TYPE_OTHER,
]
