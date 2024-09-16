import streamlit as st
from .data_operations import get_transactions, get_all_splits

@st.cache_data(ttl=300)
def load_transactions():
    return get_transactions()

@st.cache_data(ttl=300)
def load_splits():
    return get_all_splits()
