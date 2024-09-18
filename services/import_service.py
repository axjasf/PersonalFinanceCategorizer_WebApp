import pandas as pd
from typing import Dict, List, Tuple
from .data_service import load_accounts
from database.db_utils import get_session
from sqlalchemy.exc import SQLAlchemyError

def read_csv(file) -> pd.DataFrame:
    try:
        return pd.read_csv(file)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

def apply_field_mapping(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    return df.rename(columns=mapping)

def validate_data(df: pd.DataFrame) -> List[str]:
    errors = []
    required_columns = ['transaction_date', 'amount', 'description']
    for column in required_columns:
        if column not in df.columns:
            errors.append(f"Missing required column: {column}")
    return errors

def get_bank_identifier(account_name: str) -> str:
    accounts = load_accounts()
    return accounts[accounts['name'] == account_name]['bank_identifier'].iloc[0]

def process_import(file, account_name: str, field_mappings: Dict[str, Dict[str, str]]) -> Tuple[pd.DataFrame, List[str]]:
    df = read_csv(file)
    bank_identifier = get_bank_identifier(account_name)
    
    if bank_identifier not in field_mappings:
        raise ValueError(f"No field mapping found for bank identifier: {bank_identifier}")
    
    mapped_df = apply_field_mapping(df, field_mappings[bank_identifier])
    validation_errors = validate_data(mapped_df)
    
    return mapped_df, validation_errors

def insert_transactions(df: pd.DataFrame) -> bool:
    try:
        session = get_session()
        # Implement the logic to insert transactions into the database
        # This is a placeholder and needs to be implemented based on your database schema
        df.to_sql('transactions', session.bind, if_exists='append', index=False)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseError(f"Failed to insert transactions: {str(e)}")

class DatabaseError(Exception):
    pass
