import os
import streamlit as st
from api import query_assistant
from utils import get_user_info, logger

st.set_page_config(page_title="ReviewGenie: Product Review Specialist", page_icon="⭐", layout="wide")

# Ensure environment variable is set correctly
assert os.getenv('SERVING_ENDPOINT'), "SERVING_ENDPOINT must be set in app.yaml."

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Global Styles */
    .main {
        padding-top: 2rem;
    }
    
    /* Sidebar Enhancements */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #282c34 0%, #1e1e1e 100%);
    }
    
    .popular-search-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .popular-search-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Header Enhancements */
    .header-container {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(102, 126, 234, 0.1) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    .welcome-text {
        font-size: 1.1rem;
        color: #64b5f6;
        margin-top: 1rem;
        padding: 0.75rem 1.25rem;
        background: rgba(100, 181, 246, 0.1);
        border-radius: 10px;
        border-left: 4px solid #64b5f6;
    }
    
    /* Chat Message Enhancements */
    .stChatMessage {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 12px;
        animation: fadeIn 0.5s ease-in;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(30, 30, 30, 0.8);
        border-left: 4px solid #FFD700;
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
    
    /* Review Summary Cards */
    .review-summary-card {
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .positive-aspects {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(56, 142, 60, 0.1) 100%);
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .negative-aspects {
        background: linear-gradient(135deg, rgba(255, 152, 0, 0.15) 0%, rgba(244, 67, 54, 0.1) 100%);
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .positive-aspects h4, .negative-aspects h4 {
        color: #f0f0f0;
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
    }
    
    .positive-aspects ul li::marker {
        color: #4caf50;
    }
    
    .negative-aspects ul li::marker {
        color: #ff9800;
    }
    
    /* Chat Input Enhancements */
    [data-testid="stChatInputContainer"] {
        border-radius: 25px !important;
    }
    
    [data-testid="stChatInputContainer"] > div {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%) !important;
        border-radius: 25px !important;
        border: 2px solid transparent !important;
        background-image: linear-gradient(#282c34, #282c34), 
                          linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatInputContainer"]:focus-within > div {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5) !important;
        border: 2px solid transparent !important;
        background-image: linear-gradient(#282c34, #282c34), 
                          linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    [data-testid="stChatInputContainer"] input {
        color: #f0f0f0 !important;
    }
    
    [data-testid="stChatInputContainer"] input::placeholder {
        color: rgba(240, 240, 240, 0.6) !important;
    }
    
    /* Spinner Enhancement */
    .stSpinner > div {
        border-top-color: #667eea;
    }
    
    /* Typography Improvements */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }
    
    /* Better spacing for lists */
    ul, ol {
        padding-left: 1.5rem;
        line-height: 1.8;
    }
    
    /* Icon enhancements */
    .icon-wrapper {
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    /* Ensure chat input stays visible */
    [data-testid="stChatInputContainer"] {
        position: sticky !important;
        bottom: 0 !important;
        z-index: 999 !important;
        background-color: #1e1e1e !important;
        padding: 1rem 0 !important;
        margin-top: 2rem !important;
    }
    
    /* Ensure main content doesn't overlap chat input */
    .main .block-container {
        padding-bottom: 120px !important;
    }
</style>
""", unsafe_allow_html=True)

user_info = get_user_info()

# Sidebar branding and info
with st.sidebar:
    st.header("📘 About ReviewGenie")
    st.write(
        "ReviewGenie helps you find and summarize product reviews from across the web. "
        "Just type the name of a product, and I'll fetch the latest insights for you!"
    )
    
    st.markdown("### 🔍 Popular searches:")
    
    # Popular searches as clickable badges
    popular_searches = ["iPhone 15", "Dyson V15", "Sony WH-1000XM5", "Instant Pot Duo"]
    cols = st.columns(2)
    for idx, search in enumerate(popular_searches):
        with cols[idx % 2]:
            if st.button(f"🔍 {search}", key=f"popular_{idx}", use_container_width=True):
                # Store the selected search with formatted message
                formatted_query = f"looking for reviews for {search}"
                st.session_state.selected_search = formatted_query
                st.rerun()

# Main content area
st.markdown('<div class="header-container">', unsafe_allow_html=True)

# Main title and tagline
st.title("⭐ ReviewGenie")
st.markdown(
    "> **Your personal assistant for finding the best product reviews.**\n"
    "Ask about any product and get expert review summaries instantly!"
)

# Personalized greeting
if user_info.get("user_name"):
    st.markdown(f'<div class="welcome-text">Welcome, <strong>{user_info["user_name"]}</strong>! 👋</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle selected popular search - this will automatically trigger the chat processing
if "selected_search" in st.session_state and st.session_state.selected_search:
    search_query = st.session_state.selected_search
    del st.session_state.selected_search
    # Initialize messages if needed
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Add the search as a user message - this will trigger processing below
    st.session_state.messages.append({"role": "user", "content": search_query})
    st.session_state.auto_process_query = True
    st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Helper function to format messages (simplified - no automatic splitting)
def format_message_with_styling(content: str):
    """Format messages - returns content as-is without automatic positive/negative splitting"""
    # Simply return the content as markdown - let the model's response be displayed naturally
    return content

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        formatted_content = format_message_with_styling(message["content"])
        st.markdown(formatted_content, unsafe_allow_html=True)

# Process auto-queued query from popular search
prompt = None
is_auto_query = False
if "auto_process_query" in st.session_state and st.session_state.auto_process_query:
    # Get the last user message that was auto-added
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        prompt = st.session_state.messages[-1]["content"]
        is_auto_query = True
        del st.session_state.auto_process_query

# Always render chat input (ensures it stays visible) and check for new user input
user_input = st.chat_input("Ask me about reviews for any product…")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    prompt = user_input

# Process the prompt if we have one
if prompt:
    # Only display user message if it's a new input (not auto-queued, already displayed in history)
    if not is_auto_query:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching for reviews..."):
            try:
                response = query_assistant(
                    endpoint_name=os.getenv("SERVING_ENDPOINT"),
                    messages=st.session_state.messages,
                    max_tokens=400,
                )["content"]
                def stream_response(text, chunk_size=20):
                    for i in range(0, len(text), chunk_size):
                        yield text[i:i+chunk_size]
                
                # Create a placeholder for streaming
                message_placeholder = st.empty()
                full_response = ""
                for chunk in stream_response(response):
                    full_response += chunk
                    formatted_content = format_message_with_styling(full_response)
                    message_placeholder.markdown(formatted_content + "▌", unsafe_allow_html=True)
                
                # Final render without cursor
                formatted_content = format_message_with_styling(full_response)
                message_placeholder.markdown(formatted_content, unsafe_allow_html=True)
                assistant_response = full_response
            except Exception as e:
                assistant_response = "Sorry, I couldn't process your request. Please try again later."
                logger.error(f"Error querying endpoint: {e}")
                st.markdown(assistant_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
