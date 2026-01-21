import streamlit as st

def save_token(token: str):
    st.session_state["token"] = token

def get_token():
    return st.session_state.get("token")

def is_authenticated():
    return "token" in st.session_state

def logout():
    if "token" in st.session_state:
        del st.session_state["token"]
