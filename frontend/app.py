import streamlit as st
from api_client import login
from auth_utils import save_token, is_authenticated, get_token, logout

st.set_page_config(page_title="RBAC Login", layout="centered")

st.title("RBAC System – Login")

if not is_authenticated():
    username = st.text_input("Enter username", placeholder="admin / employee / manager")

    if st.button("Login"):
        result = login(username)

        if "token" in result and result["token"] != "invalid-token":
            save_token(result["token"])
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username")
else:
    st.success("You are logged in")

    token = get_token()

    role = "Unknown"
    if "admin" in token:
        role = "Admin"
    elif "employee" in token:
        role = "Employee"
    elif "manager" in token:
        role = "Manager"

    st.subheader("User Profile")
    st.write(f"**Role:** {role}")

    if st.button("Logout"):
        logout()
        st.rerun()

