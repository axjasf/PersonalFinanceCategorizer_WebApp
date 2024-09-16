# database/db_utils.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from config import DATABASE_URI  # Import the DATABASE_URI from config.py

engine = create_engine(DATABASE_URI, echo=True)  # Set echo=True for debugging
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)

def get_session():
    return session
