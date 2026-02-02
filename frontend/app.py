import streamlit as st
import requests
from api_client import login
from auth_utils import save_token, is_authenticated, get_token, logout
from jose import jwt
import time

# Configure page with custom theme
st.set_page_config(
    page_title="Clara - Company AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --background: #0f172a;
        --text-color: #f1f5f9;
    }
    
    /* Login page styling */
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 3rem;
        background: linear-gradient(145deg, #1e293b, #334155);
        border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        text-align: center;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Custom button styling */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    
    /* Success message styling */
    .stSuccess {
        border-radius: 10px;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #f1f5f9;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Animated gradient title */
    .gradient-title {
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
    }
    
    /* Card styling */
    .card {
        background: linear-gradient(145deg, #1e293b, #334155);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    /* Source chip styling */
    .source-chip {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 20px;
        font-size: 0.75rem;
        margin: 0.25rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://localhost:8000"

def get_user_info():
    """Decode JWT token to get user info"""
    token = get_token()
    if token:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return {
                "username": payload.get("sub", "User"),
                "role": payload.get("role", "Unknown"),
                "department": payload.get("department", "Unknown")
            }
        except Exception as e:
            return {"username": "User", "role": "Unknown", "department": "Unknown"}
    return {"username": "User", "role": "Unknown", "department": "Unknown"}

def render_login_page():
    """Render a beautiful login page"""
    st.markdown("""
    <div class="login-container">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🤖</div>
        <h1 class="gradient-title">Clara - Company AI Assistant</h1>
        <p style="color: #94a3b8; margin-bottom: 2rem;">Your Enterprise Knowledge Companion</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            st.markdown("### 🔐 Secure Login")
            st.markdown("---")
            
            username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Sign In", use_container_width=True, type="primary"):
                if username and password:
                    result = login(username, password)
                    if "access_token" in result:
                        save_token(result["access_token"])
                        st.success("Welcome aboard! 🎉")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('detail', 'Login failed')}")
                else:
                    st.warning("Please enter both username and password")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; margin-top: 2rem; color: #64748b;">
                <small>powered by group 2 interns of Infosys springboard internship</small>
            </div>
            """, unsafe_allow_html=True)

def render_chat_interface():
    """Render a beautiful chat interface"""
    user_info = get_user_info()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">👤</div>
            <h3 style="margin: 0.5rem 0; color: #ffffff;">{}</h3>
        </div>
        """.format(user_info["username"]), unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()
    
    # Main chat area
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 class="gradient-title">💬 Clara - Company AI Assistant</h1>
        <p style="color: #94a3b8;">Ask me anything about company policies, procedures, and documentation</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant" and "sources" in message and message["sources"]:
                st.markdown("<div style='margin-top: 0.5rem;'>", unsafe_allow_html=True)
                for source in message["sources"]:
                    st.markdown(f'<span class="source-chip">📄 {source}</span>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask me anything, always ready to help"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Clara is thinking..."):
                token = get_token()
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/chat",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {token}"
                        },
                        json={"query": prompt},
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("answer", "I couldn't find an answer to that question.")
                        sources = data.get("sources", [])
                        
                        st.markdown(answer)
                        
                        if sources:
                            st.markdown("<div style='margin-top: 0.5rem;'>", unsafe_allow_html=True)
                            for source in sources:
                                st.markdown(f'<span class="source-chip">📄 {source}</span>', unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        })
                    else:
                        error_msg = response.json().get("detail", "Unknown error")
                        st.error(f"❌ {error_msg}")
                        
                except Exception as e:
                    st.error(f"🚨 Connection error: {str(e)}")

# Main app flow
if not is_authenticated():
    render_login_page()
else:
    render_chat_interface()
