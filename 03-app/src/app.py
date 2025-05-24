import os
import streamlit as st
from api import query_assistant
from utils import get_user_info, logger

st.set_page_config(page_title="ReviewGenie: Product Review Specialist", page_icon="⭐")

# Ensure environment variable is set correctly
assert os.getenv('SERVING_ENDPOINT'), "SERVING_ENDPOINT must be set in app.yaml."

user_info = get_user_info()

# Sidebar branding and info
with st.sidebar:
    st.header("About ReviewGenie")
    st.write(
        "ReviewGenie helps you find and summarize product reviews from across the web. "
        "Just type the name of a product, and I'll fetch the latest insights for you!"
    )
    st.markdown("**Popular searches:**\n- iPhone 15\n- Dyson V15\n- Sony WH-1000XM5\n- Instant Pot Duo")

# Main title and tagline
st.title("⭐ ReviewGenie")
st.markdown(
    "> **Your personal assistant for finding the best product reviews.**\n"
    "Ask about any product and get expert review summaries instantly!"
)

# Personalized greeting
if user_info.get("user_name"):
    st.markdown(f"Welcome, **{user_info['user_name']}**! 👋")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input with branded prompt
if prompt := st.chat_input("Ask me about reviews for any product…"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = query_assistant(
                    endpoint_name=os.getenv("SERVING_ENDPOINT"),
                    messages=st.session_state.messages,
                    max_tokens=400,
                )["content"]
                def stream_response(text, chunk_size=20):
                    for i in range(0, len(text), chunk_size):
                        yield text[i:i+chunk_size]
                st.write_stream(stream_response(response))
                assistant_response = response
            except Exception as e:
                assistant_response = "Sorry, I couldn't process your request. Please try again later."
                logger.error(f"Error querying endpoint: {e}")
                st.markdown(assistant_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
