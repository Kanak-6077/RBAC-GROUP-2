import streamlit as st
from frontend.api_client import send_chat_query

def render_chat():
    st.title("Company Knowledge Chat")

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
