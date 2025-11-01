import sys
import os
# Add project root to sys.path BEFORE any imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import requests
from src.frontend_src.config.frontend_settings import Settings

settings = Settings()

# Page Configuration
st.set_page_config(
    page_title="AstraRAG - Intelligent Assistant",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for stunning visual design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #FEFEFE 0%, #F8F8F8 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Title styling with gradient and glow */
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.8rem;
        font-weight: 600;
        text-align: center;
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -2.5px;
    }
    
    @keyframes glow {
        from {
            filter: drop-shadow(0 0 12px rgba(212, 175, 55, 0.4));
        }
        to {
            filter: drop-shadow(0 0 24px rgba(212, 175, 55, 0.7));
        }
    }
    
    .subtitle {
        text-align: center;
        color: #666666;
        font-size: 1rem;
        margin-bottom: 4rem;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Chat message containers */
    .stChatMessage {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid #E8E8E8 !important;
        padding: 2rem !important;
        margin-bottom: 1.5rem !important;
        transition: all 0.25s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    
    .stChatMessage:hover {
        border-color: #D4AF37 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    }
    
    /* User message styling */
    [data-testid="stChatMessageContent"] {
        color: #1a1a1a !important;
        font-size: 1.05rem;
        line-height: 1.75;
        font-weight: 400;
    }
    
    [data-testid="stChatMessageContent"] * {
        color: #1a1a1a !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: #1a1a1a !important;
    }
    
    [data-testid="stChatMessageContent"] code {
        color: #1a1a1a !important;
        background: #F5F5F5 !important;
    }
    
    /* Chat input styling */
    .stChatInput {
        border-radius: 24px !important;
        background: #FFFFFF !important;
        border: 1.5px solid #E0E0E0 !important;
        transition: all 0.25s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .stChatInput:focus-within {
        border-color: #D4AF37 !important;
        box-shadow: 0 4px 16px rgba(212, 175, 55, 0.12);
    }
    
    /* Chat input text color */
    .stChatInput input {
        color: #1a1a1a !important;
    }
    
    .stChatInput textarea {
        color: #1a1a1a !important;
    }
    
    .stChatInput input::placeholder {
        color: #999999 !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #999999 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #FAFAFA !important;
        border-radius: 12px !important;
        border: 1px solid #E8E8E8 !important;
        color: #666666 !important;
        font-weight: 500 !important;
        transition: all 0.25s ease;
        padding: 0.75rem 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F5F5F5 !important;
        border-color: #D4AF37 !important;
        color: #1a1a1a !important;
    }
    
    .streamlit-expanderContent {
        background: #FFFFFF !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid #E8E8E8 !important;
        border-top: none !important;
        padding: 1.25rem !important;
    }
    
    /* Sources badge styling */
    .sources-badge {
        display: inline-block;
        background: #FAFAFA;
        border: 1px solid #E0E0E0;
        padding: 0.5rem 1rem;
        border-radius: 24px;
        font-size: 0.85rem;
        color: #666666;
        margin-top: 1rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Details content styling */
    .detail-item {
        background: #FAFAFA;
        border-left: 2px solid #D4AF37;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        border-radius: 4px;
        color: #1a1a1a;
    }
    
    .detail-label {
        color: #D4AF37;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.4rem;
    }
    
    /* Avatar styling */
    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #2d2d2d, #1a1a1a) !important;
    }
    
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #D4AF37, #C09D2E) !important;
    }
    
    /* Error message styling */
    .error-message {
        background: #FFF5F5;
        border: 1px solid #FFE0E0;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #CC0000;
        margin-top: 0.75rem;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Markdown content styling */
    .stMarkdown {
        color: #1a1a1a !important;
    }
    
    .stMarkdown * {
        color: #1a1a1a !important;
    }
    
    .stMarkdown p {
        color: #1a1a1a !important;
    }
    
    .stMarkdown code {
        color: #1a1a1a !important;
        background: #F5F5F5 !important;
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    .stMarkdown a {
        color: #D4AF37 !important;
        text-decoration: none;
        border-bottom: 1px solid #D4AF37;
        transition: all 0.25s ease;
    }
    
    .stMarkdown a:hover {
        color: #1a1a1a !important;
        border-bottom-color: #1a1a1a;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F5F5F5;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #D4AF37;
        border-radius: 8px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #C09D2E;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🌌 AstraRAG</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Intelligent Agentic RAG Assistant</p>', unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message.get("role") == "assistant":
            sources = message.get("sources", [])
            tool_used = message.get("tool_used")
            rationale = message.get("rationale")
            
            # Display sources as badges
            if sources:
                sources_text = ", ".join([f"`{src}`" for src in sources])
                st.markdown(f'<div class="sources-badge">📚 Sources: {sources_text}</div>', unsafe_allow_html=True)
            
            # Display tool and rationale in expandable section
            if tool_used or rationale:
                with st.expander("🔍 View Technical Details"):
                    st.markdown(f"""
                    <div class="detail-item">
                        <div class="detail-label">🛠️ Tool Used</div>
                        <div>{tool_used if tool_used else 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">💭 Rationale</div>
                        <div>{rationale if rationale else 'N/A'}</div>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
user_prompt = st.chat_input("💬 Ask me anything...")

if user_prompt:
    # Display user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Prepare payload for API
    payload = {"chat_history": st.session_state.chat_history}
    
    # Show loading state
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = requests.post(settings.CHAT_ENDPOINT_URL, json=payload, timeout=30)
                response.raise_for_status()
                response_json = response.json()
                
                assistant_response = response_json.get("answer", "(No response)")
                tool_used = response_json.get("tool_used", "N/A")
                rationale = response_json.get("rationale", "N/A")
                sources = response_json.get("sources", [])
                
            except requests.exceptions.ConnectionError:
                assistant_response = "🔌 **Connection Error**\n\nCouldn't connect to the backend server. Please ensure:\n- The backend server is running on the correct port\n- Check your `frontend_settings.py` configuration"
                tool_used = "N/A"
                rationale = "Backend server is not accessible"
                sources = []
                st.markdown(f'<div class="error-message">💡 **Tip:** Start your backend server with `uvicorn main:app --reload --port 8000`</div>', unsafe_allow_html=True)
            except requests.exceptions.Timeout:
                assistant_response = "⏱️ **Request Timeout**\n\nThe server took too long to respond. Please try again."
                tool_used = "N/A"
                rationale = "Request exceeded 30 second timeout"
                sources = []
            except requests.exceptions.HTTPError as e:
                assistant_response = f"❌ **Server Error**\n\nThe server returned an error (Status: {e.response.status_code})"
                tool_used = "N/A"
                rationale = f"HTTP Error: {str(e)}"
                sources = []
                st.markdown(f'<div class="error-message">Technical details: {str(e)}</div>', unsafe_allow_html=True)
            except Exception as e:
                assistant_response = f"⚠️ **Unexpected Error**\n\nAn unexpected error occurred while processing your request."
                tool_used = "N/A"
                rationale = f"Error: {str(e)}"
                sources = []
                st.markdown(f'<div class="error-message">Technical details: {str(e)}</div>', unsafe_allow_html=True)

    # Save and display assistant response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_response,
        "tool_used": tool_used,
        "rationale": rationale,
        "sources": sources
    })
    
    # Rerun to display the new message properly
    st.rerun()