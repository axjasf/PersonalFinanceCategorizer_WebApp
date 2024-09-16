"""
Main entry point for the Personal Finance Categorizer application.
This file sets up the Streamlit configuration and provides the main page layout.
It also initializes the database and serves as the starting point for the app.
"""

import streamlit as st
from database.db_utils import init_db

# Initialize the database
init_db()

st.set_page_config(
    page_title="Personal Finance Categorizer",
    page_icon="💰",
    layout="wide"
)

st.title("Personal Finance Categorizer")

st.write("""
Welcome to your Personal Finance Categorizer. 
Use the sidebar to navigate through different sections of the application.
""")

# You can add any common functionality or overview here
