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
    page_title="VeriRAG - Intelligent Assistant",
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
        background: linear-gradient(180deg, #0A1A2F 0%, #0d1f36 50%, #0A1A2F 100%);
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
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #D4AF37 0%, #F4E4A6 50%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1.5px;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from {
            filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.4));
            transform: translateY(0);
        }
        to {
            filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.6));
            transform: translateY(-2px);
        }
    }
    
    .subtitle {
        text-align: center;
        color: #B8C5D6;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 400;
        letter-spacing: 0.8px;
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Chat message containers */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(212, 175, 55, 0.15) !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stChatMessage:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        border-color: rgba(212, 175, 55, 0.3) !important;
        transform: translateY(-2px) translateZ(0);
        box-shadow: 0 12px 40px rgba(212, 175, 55, 0.15);
    }
    
    /* User message styling */
    [data-testid="stChatMessageContent"] {
        color: #FFFFFF;
        font-size: 1rem;
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* Chat input styling */
    .stChatInput {
        border-radius: 6px !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
        border: 2px solid rgba(212, 175, 55, 0.2) !important;
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stChatInput:focus-within {
        border-color: rgba(212, 175, 55, 0.6) !important;
        box-shadow: 0 4px 24px rgba(212, 175, 55, 0.2);
        transform: translateY(-1px);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.08) 0%, rgba(212, 175, 55, 0.04) 100%) !important;
        border-radius: 6px !important;
        border: 1px solid rgba(212, 175, 55, 0.15) !important;
        color: #D4AF37 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.12) 0%, rgba(212, 175, 55, 0.06) 100%) !important;
        border-color: rgba(212, 175, 55, 0.3) !important;
        transform: translateX(4px);
    }
    
    .streamlit-expanderContent {
        background: rgba(0, 0, 0, 0.2) !important;
        border-radius: 0 0 6px 6px !important;
        border: 1px solid rgba(212, 175, 55, 0.1) !important;
        border-top: none !important;
    }
    
    /* Sources badge styling */
    .sources-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(212, 175, 55, 0.08));
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #D4AF37;
        margin-top: 0.8rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .sources-badge:hover {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(212, 175, 55, 0.12));
        transform: translateY(-1px);
    }
    
    /* Details content styling */
    .detail-item {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
        border-left: 3px solid #D4AF37;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        border-radius: 4px;
        color: #FFFFFF;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .detail-item:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.02) 100%);
        transform: translateX(4px);
    }
    
    .detail-label {
        color: #D4AF37;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.4rem;
    }
    
    /* Avatar styling */
    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #D4AF37, #C5A028) !important;
    }
    
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #0A1A2F, #1a3a5f) !important;
        border: 2px solid #D4AF37 !important;
    }
    
    /* Error message styling */
    .error-message {
        background: rgba(245, 87, 108, 0.1);
        border: 1px solid rgba(245, 87, 108, 0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #ffb3c1;
        margin-top: 0.5rem;
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
        color: #FFFFFF;
        font-weight: 400;
    }
    
    .stMarkdown a {
        color: #D4AF37;
        text-decoration: none;
        border-bottom: 1px solid rgba(212, 175, 55, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
    }
    
    .stMarkdown a:hover {
        color: #F4E4A6;
        border-bottom-color: rgba(244, 228, 166, 0.5);
        transform: translateY(-1px);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #D4AF37, #C5A028);
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #F4E4A6, #D4AF37);
    }
    
    /* Button hover effects */
    button {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    button:hover {
        transform: translateY(-2px) !important;
    }
    
    /* Micro-animations for premium feel */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .stChatMessage {
        animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">✨ VeriRAG</h1>', unsafe_allow_html=True)
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