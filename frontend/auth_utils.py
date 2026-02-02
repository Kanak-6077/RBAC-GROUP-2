import streamlit as st

def save_token(token: str):
    st.session_state["token"] = token

def get_token():
    return st.session_state.get("token")

def is_authenticated():
    return "token" in st.session_state

def logout():
    # Clear all session state items for a fresh login
    keys_to_clear = ["token", "messages", "user_info"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
