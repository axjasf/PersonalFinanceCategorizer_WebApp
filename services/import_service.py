import pandas as pd
from typing import Dict, List, Tuple
from .data_service import load_accounts, get_or_create_payee
from database.db_utils import get_session
from sqlalchemy import text


def read_csv(file) -> pd.DataFrame:
    try:
        return pd.read_csv(file)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")


def apply_field_mapping(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    return df.rename(columns=mapping)


def validate_data(df: pd.DataFrame) -> List[str]:
    errors = []
    required_columns = ["transaction_date", "amount", "description"]
    for column in required_columns:
        if column not in df.columns:
            errors.append(f"Missing required column: {column}")
    return errors


def get_bank_identifier(account_name: str) -> str:
    accounts = load_accounts()
    return accounts[accounts["name"] == account_name]["bank_identifier"].iloc[0]


def process_import(
    file, account_name: str, field_mappings: Dict[str, Dict[str, str]]
) -> Tuple[pd.DataFrame, List[str]]:
    df = read_csv(file)
    bank_identifier = get_bank_identifier(account_name)

    if bank_identifier not in field_mappings:
        raise ValueError(f"No field mapping found for bank identifier: {bank_identifier}")

    mapped_df = apply_field_mapping(df, field_mappings[bank_identifier])
    validation_errors = validate_data(mapped_df)

    return mapped_df, validation_errors


def insert_transactions(df):
    session = get_session()
    try:
        # Only insert the columns that exist in the transactions table
        table_columns = session.execute(text("SELECT * FROM transactions LIMIT 0")).keys()
        df_to_insert = df.reindex(columns=table_columns, fill_value=None)

        # Ensure payee_id is an integer
        if "payee_id" in df_to_insert.columns:
            df_to_insert["payee_id"] = df_to_insert["payee_id"].astype(int)

        df_to_insert.to_sql("transactions", session.bind, if_exists="append", index=False)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise DatabaseError(f"Failed to insert transactions: {str(e)}")


class DatabaseError(Exception):
    pass


def process_commerzbank(
    transactions_df: pd.DataFrame, exchange_rates_df: pd.DataFrame
) -> pd.DataFrame:
    # Ensure date columns are in datetime format
    transactions_df["Date"] = pd.to_datetime(transactions_df["Transaction date"], format="%d.%m.%Y")
    exchange_rates_df["Date"] = pd.to_datetime(exchange_rates_df["Date"])

    # Merge transactions with exchange rates
    df = transactions_df.merge(exchange_rates_df[["Date", "Close"]], on="Date", how="left")

    # Convert amount to USD
    df["Amount (USD)"] = df["Amount"] * df["Close"]

    # Clean up
    df = df.drop(columns=["Transaction date", "Close"])
    df = df.rename(columns={"Amount": "Amount (EUR)", "Amount (USD)": "Amount"})

    return df


def process_bank_file(
    bank: str, transactions_file, exchange_rates_file, field_mappings: Dict[str, Dict]
) -> pd.DataFrame:
    transactions_df = read_csv(transactions_file)

    if bank not in field_mappings:
        raise ValueError(f"No field mapping found for bank: {bank}")

    bank_config = field_mappings[bank]
    fields = bank_config["fields"]

    # Rename columns based on field mappings
    transactions_df = transactions_df.rename(columns={v: k for k, v in fields.items()})

    # Handle payee
    if "payee" in fields:
        transactions_df["payee_id"] = transactions_df["payee"].apply(get_or_create_payee)
        transactions_df = transactions_df.drop(columns=["payee"])

    # Ensure 'amount' column exists
    if "amount" not in transactions_df.columns:
        raise ValueError(f"'amount' column is missing after field mapping for bank: {bank}")

    if bank_config.get("needs_currency_conversion", False):
        if exchange_rates_file is None:
            raise ValueError("Exchange rates file is required for currency conversion")
        exchange_rates_df = read_csv(exchange_rates_file)
        transactions_df = process_currency_conversion(
            transactions_df,
            exchange_rates_df,
            bank_config["from_currency"],
            bank_config["to_currency"],
        )

    return transactions_df


def process_currency_conversion(
    transactions_df: pd.DataFrame,
    exchange_rates_df: pd.DataFrame,
    from_currency: str,
    to_currency: str,
) -> pd.DataFrame:
    # Ensure date columns are in datetime format
    transactions_df["transaction_date"] = pd.to_datetime(transactions_df["transaction_date"])
    exchange_rates_df["Date"] = pd.to_datetime(exchange_rates_df["Date"])

    # Merge transactions with exchange rates
    df = transactions_df.merge(
        exchange_rates_df[["Date", "Close"]],
        left_on="transaction_date",
        right_on="Date",
        how="left",
    )

    # Convert amount to target currency
    df[f"amount_{to_currency}"] = df["amount"] * df["Close"]

    # Clean up
    df = df.drop(columns=["Close", "Date"])
    df = df.rename(columns={"amount": f"amount_{from_currency}", f"amount_{to_currency}": "amount"})

    return df
