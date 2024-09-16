import streamlit as st

def get_grid_key(key_name):
    if key_name not in st.session_state:
        st.session_state[key_name] = 0
    return st.session_state[key_name]

def increment_grid_key(key_name):
    if key_name not in st.session_state:
        st.session_state[key_name] = 0
    st.session_state[key_name] += 1
