import logging
import streamlit as st

def get_user_info():
    headers = st.context.headers
    return dict(
        user_name=headers.get("X-Forwarded-Preferred-Username"),
        user_email=headers.get("X-Forwarded-Email"),
        user_id=headers.get("X-Forwarded-User"),
    )

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 