# How to use this script:
#
# This script performs a performance test on the database by generating and inserting
# a specified number of transactions and their associated splits.
#
# To run the script, use the following command in your terminal:
#
# python generate_performance_test_data.py [options]
#
# Available options:
# --transactions INT    Number of transactions to generate (default: 1000)
# --avg-splits FLOAT    Average number of splits per transaction (default: 2)
# --max-splits INT      Maximum number of splits per transaction (default: 5)
# --drop                If specified, drops existing data before inserting new data
#
# Example usage:
# python generate_performance_test_data.py --transactions 10000 --avg-splits 3 --max-splits 7 --drop
#
# This command will:
# 1. Drop existing data from the transactions and transaction_splits tables (if --drop is specified)
# 2. Generate 10,000 random transactions
# 3. For each transaction, generate between 1 and 7 splits, with an average of 3 splits
# 4. Insert all generated data into the database
# 5. Report the time taken to complete the operation
#
# Note: This script uses only existing payees, accounts, and categories from your database.
# Make sure you have some data in these tables before running the script.
#
# The script uses the DATABASE_URI from your config.py file. Make sure this is set correctly before running the script.
#
# After running the script, check the console output for performance metrics and any error messages.

import sqlite3
import random
from datetime import datetime, timedelta
import argparse
import logging
from config import DATABASE_URI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    return sqlite3.connect(DATABASE_URI.replace("sqlite:///", ""))


def drop_all_data(cursor):
    tables = ["transactions", "transaction_splits"]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
    logger.info("All data deleted from transactions and transaction_splits tables.")


def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)


def get_existing_ids(cursor, table):
    cursor.execute(f"SELECT id FROM {table}")
    return [row[0] for row in cursor.fetchall()]


def generate_transactions(cursor, num_transactions, avg_splits, max_splits):
    start_date = datetime(2020, 1, 1).date()
    end_date = datetime(2023, 12, 31).date()

    payee_ids = get_existing_ids(cursor, "payees")
    account_ids = get_existing_ids(cursor, "accounts")
    category_ids = get_existing_ids(cursor, "categories")

    transactions = []
    splits = []

    for _ in range(num_transactions):
        transaction_date = generate_random_date(start_date, end_date)
        amount = round(random.uniform(1, 1000), 2)
        payee_id = random.choice(payee_ids)
        account_id = random.choice(account_ids)
        description = f"Transaction {_+1}"

        transactions.append((transaction_date, amount, payee_id, account_id, description))

        num_splits = min(max(1, int(random.gauss(avg_splits, 1))), max_splits)
        remaining_amount = amount

        for i in range(num_splits):
            if i == num_splits - 1:
                split_amount = remaining_amount
            else:
                split_amount = round(random.uniform(0.01, remaining_amount - 0.01), 2)

            category_id = random.choice(category_ids)
            splits.append((_ + 1, category_id, split_amount))
            remaining_amount -= split_amount

    return transactions, splits


def insert_data(cursor, transactions, splits):
    cursor.executemany(
        """
        INSERT INTO transactions (transaction_date, amount, payee_id, account_id, description)
        VALUES (?, ?, ?, ?, ?)
    """,
        transactions,
    )

    cursor.executemany(
        """
        INSERT INTO transaction_splits (transaction_id, category_id, allocated_amount)
        VALUES (?, ?, ?)
    """,
        splits,
    )


def run_performance_test(num_transactions, avg_splits, max_splits, drop_existing):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if drop_existing:
            drop_all_data(cursor)

        start_time = datetime.now()

        transactions, splits = generate_transactions(
            cursor, num_transactions, avg_splits, max_splits
        )

        insert_data(cursor, transactions, splits)

        conn.commit()

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.info(f"Performance test completed in {duration: .2f} seconds")
        logger.info(f"Inserted {num_transactions} transactions and {len(splits)} splits")

    except Exception as e:
        logger.error(f"Error during performance test: {str(e)}")
        conn.rollback()
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Database performance test")
    parser.add_argument(
        "--transactions", type=int, default=1000, help="Number of transactions to generate"
    )
    parser.add_argument(
        "--avg-splits", type=float, default=2, help="Average number of splits per transaction"
    )
    parser.add_argument(
        "--max-splits", type=int, default=5, help="Maximum number of splits per transaction"
    )
    parser.add_argument("--drop", action="store_true", help="Drop existing data before inserting")
    args = parser.parse_args()

    run_performance_test(args.transactions, args.avg_splits, args.max_splits, args.drop)


if __name__ == "__main__":
    main()
