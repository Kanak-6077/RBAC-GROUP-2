import requests

API_BASE_URL = "http://127.0.0.1:8000"

def login(username: str):
    response = requests.post(
        f"{API_BASE_URL}/login",
        params={"username": username}
    )
    return response.json()
