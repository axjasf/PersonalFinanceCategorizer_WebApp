import sqlite3
import os
from config import DATABASE_URI

def execute_sql_file(cursor, sql_file):
    with open(sql_file, 'r') as file:
        sql_script = file.read()
    cursor.executescript(sql_script)
    print(f"Executed SQL file: {sql_file}")

def init_db():
    # Extract the database file path from the URI
    db_path = DATABASE_URI.replace('sqlite:///', '')
    
    print(f"Attempting to connect to database at: {db_path}")
    
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
        print(f"Created directory: {os.path.dirname(db_path)}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute your SQL scripts
    execute_sql_file(cursor, 'data/tables/basic.sql')
    execute_sql_file(cursor, 'data/tables/transactions.sql')
    execute_sql_file(cursor, 'data/tables/orders.sql')
    execute_sql_file(cursor, 'data/example_data/sample_basic.sql')
    execute_sql_file(cursor, 'data/example_data/sample_transactions_and_orders.sql')

    conn.commit()
    conn.close()

    print("Database initialization complete.")

    # Verify data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    print(f"Number of transactions in the database: {count}")
    conn.close()

if __name__ == "__main__":
    init_db()
