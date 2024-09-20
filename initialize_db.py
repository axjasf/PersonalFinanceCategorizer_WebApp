"""
Database initialization script for the Personal Finance Categorizer.
This script creates the necessary tables and populates them with sample data.
It should be run once to set up the database before starting the application.
"""

import sqlite3
import os
from config import DATABASE_URI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def execute_sql_file(cursor, sql_file):
    with open(sql_file, "r") as file:
        sql_script = file.read()
    cursor.executescript(sql_script)
    logger.info(f"Executed SQL file: {sql_file}")


def init_db():
    # Extract the database file path from the URI
    db_path = DATABASE_URI.replace("sqlite:///", "")

    logger.info(f"Attempting to connect to database at: {db_path}")

    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
        logger.info(f"Created directory: {os.path.dirname(db_path)}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Execute table creation scripts
        for sql_file in os.listdir("data/tables"):
            if sql_file.endswith(".sql"):
                execute_sql_file(cursor, os.path.join("data/tables", sql_file))

        # Execute view creation scripts
        for sql_file in os.listdir("data/views"):
            if sql_file.endswith(".sql"):
                execute_sql_file(cursor, os.path.join("data/views", sql_file))

        # Execute sample data scripts (optional, comment out if not needed)
        for sql_file in os.listdir("data/example_data"):
            if sql_file.endswith(".sql"):
                execute_sql_file(cursor, os.path.join("data/example_data", sql_file))

        conn.commit()
        logger.info("Database initialization complete.")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

    # Verify data (optional)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    logger.info(f"Number of transactions in the database: {count}")
    conn.close()


def init_test_db():
    # Use an in-memory SQLite database for testing
    global DATABASE_URI
    DATABASE_URI = "sqlite:///:memory:"
    init_db()


if __name__ == "__main__":
    init_db()
