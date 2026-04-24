import streamlit as st

def check_auth():
    """No-op authentication. Always returns True."""
    st.session_state.authenticated = True
    if 'user_email' not in st.session_state:
        st.session_state.user_email = "guest@nexus.ai"
    return True

def render_login_page():
    """No-op login page."""
    pass

def logout():
    """No-op logout."""
    st.session_state.authenticated = False
    st.rerun()
