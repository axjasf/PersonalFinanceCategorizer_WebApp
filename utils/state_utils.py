"""
Streamlit state management utilities for the Personal Finance Categorizer.
Provides functions to manage and update session state variables,
particularly for maintaining grid states across reruns.
"""

import streamlit as st

def get_grid_key(key_name):
    print(f"Accessing key: {key_name}")
    print(f"Session state keys: {st.session_state.keys()}")
    if key_name not in st.session_state:
        print(f"Initializing {key_name} in session state")
        st.session_state[key_name] = 0
    return st.session_state[key_name]

def increment_grid_key(key_name):
    if key_name not in st.session_state:
        st.session_state[key_name] = 0
    st.session_state[key_name] += 1
