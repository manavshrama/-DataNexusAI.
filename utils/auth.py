import streamlit as st
import time
from utils.theme import load_css, glass_card

def check_auth():
    """Returns True if user is authenticated, else renders login and returns False."""
    if st.session_state.get("authenticated", False):
        return True
    
    render_login_page()
    return False

def render_login_page():
    load_css()
    
    # Center the login card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("<div style='margin-top: 15vh;'></div>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""
                <div class="glass-card" style="padding: 3rem; text-align: center; max-width: 450px; margin: 0 auto;">
                    <img src="https://img.icons8.com/nolan/128/artificial-intelligence.png" width="100" style="margin-bottom: 1rem;">
                    <h1 class="gradient-text" style="font-size: 2.5rem; margin-bottom: 0.5rem;">Nexus Access</h1>
                    <p style="opacity: 0.6; margin-bottom: 2rem;">Authenticate securely using your Google Workspace</p>
                    
                    <!-- Simulated Google Auth Button -->
                    <div style="margin-top: 1rem;">
            """, unsafe_allow_html=True)
            
            # Simple Email Input Form
            with st.form("email_login_form"):
                email_input = st.text_input("Email Address", placeholder="e.g., operator@gmail.com")
                submitted = st.form_submit_button("🚀 Enter Nexus", use_container_width=True, type="primary")
                
                if submitted:
                    if "@" in email_input and "." in email_input:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email_input
                        st.success(f"Welcome, {email_input}! Initializing Neural Forge...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Please enter a valid email address to proceed.")
            
            st.markdown("""
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <p style="text-align: center; opacity: 0.3; font-size: 0.8rem; margin-top: 2rem;">
                    DataNexus AI | Secure Environment Protocol 1.2.0 <br>
                    <i>Note: Real OAuth requires Google Cloud Client IDs</i>
                </p>
            """, unsafe_allow_html=True)

def logout():
    st.session_state.authenticated = False
    st.rerun()
