import streamlit as st
from frontend.api_client import send_chat_query
import sys
import os

# Use relative import to avoid ModuleNotFoundError
try:
    from .api_client import send_chat_query
except ImportError:
    try:
        from api_client import send_chat_query
    except ImportError as e:
        print(f"DIAGNOSTIC ERROR: Both import methods failed: {e}")
        # Define a fallback function to prevent NameError
        def send_chat_query(query_text):
            return {"answer": "Import error - please restart the app"}

# Import auth utilities for authentication check
from .auth_utils import is_authenticated

def render_chat():
    st.title("Company Knowledge Chat")

    # Check authentication before proceeding
    if not is_authenticated():
        st.error("Please log in to use the chat.")
        st.stop()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input box
    user_input = st.chat_input("Ask something...")

    if user_input:
        # Show user message
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_chat_query(user_input)

                if "answer" in response:
                    answer = response["answer"]
                    sources = response.get("sources", [])

                    st.markdown(answer)

                    if sources:
                        st.markdown("**Sources:**")
                        for s in sources:
                            st.markdown(f"- {s}")

                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )
                else:
                    st.error("No response from server.")
