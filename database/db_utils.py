# database/db_utils.py
"""
Database utility functions for the Personal Finance Categorizer.
Provides functions for initializing the database connection, creating sessions,
and other database-related operations used throughout the application.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .models import Base
from config import DATABASE_URI  # Import the DATABASE_URI from config.py
import os

engine = create_engine(DATABASE_URI, echo=True)  # Set echo=True for debugging
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    # Create all tables defined in SQLAlchemy models
    Base.metadata.create_all(engine)

    # Create a session
    session = get_session()

    try:
        # Execute view creation scripts
        views_dir = os.path.join(os.path.dirname(__file__), "..", "data", "views")
        for sql_file in os.listdir(views_dir):
            if sql_file.endswith(".sql"):
                view_path = os.path.join(views_dir, sql_file)
                with open(view_path, "r") as file:
                    view_sql = file.read()
                    print(f"Executing view creation script: {sql_file}")
                    # Split the SQL into separate statements
                    statements = view_sql.split(";")
                    for statement in statements:
                        # Remove any leading/trailing whitespace and skip empty statements
                        statement = statement.strip()
                        if statement:
                            session.execute(text(statement))

        # Commit the changes
        session.commit()
        print("Database initialization complete, including views.")

    except Exception as e:
        print(f"Error during database initialization: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()


def get_session():
    return Session()
