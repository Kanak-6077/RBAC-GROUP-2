import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"

def login(username: str):
    response = requests.post(
        f"{API_BASE_URL}/login",
        params={"username": username}
    )
    return response.json()

# NEW FUNCTION for Task 2 (Chat)
def send_chat_query(query: str):
    token = st.session_state.get("token")

    if not token:
        return {"answer": "You are not logged in."}

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        f"{API_BASE_URL}/chat",
        json={"query": query},
        headers=headers
    )

    if response.status_code != 200:
        return {"answer": "Error contacting backend."}

    return response.json()
