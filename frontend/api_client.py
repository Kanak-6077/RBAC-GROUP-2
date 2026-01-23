import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"

def login(username, password):
    response = requests.post(
        f"{API_BASE_URL}/login",
        json={"username": username, "password": password}
    )
    response.raise_for_status()
    return response.json()

def handle_login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            result = login(username, password)
            st.session_state["token"] = result["access_token"]
            st.session_state["user_info"] = result.get("user")
            st.success("Logged in successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

def send_chat_query(query_text):
    token = st.session_state.get("token")
    if not token:
        return {"answer": "Authentication required."}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"query": query_text},
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        return {"answer": f"Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"answer": f"Connection error: {e}"}