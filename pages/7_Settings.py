import streamlit as st
from utils.theme import load_css, glass_card
from utils.navigation import sidebar_nav

st.set_page_config(page_title="DataNexusAI - Settings", page_icon="⚙️", layout="wide")
load_css()
sidebar_nav(6) # Settings is the 7th item (index 6)

st.markdown('<h1 class="gradient-text">System Configuration</h1>', unsafe_allow_html=True)
st.caption("Manage your DataNexus AI environment and security.")

# Initialize settings in session state if not present
if 'settings' not in st.session_state:
    st.session_state['settings'] = {'api_key': '', 'theme': 'Nexus Noir (Dark)'}

# API Keys Section
st.write("## ")
with st.container():
    st.markdown("""
    <div class="glass-card">
        <h3>🔑 API Integration</h3>
        <p style="opacity: 0.6; font-size: 0.9rem;">Configure your keys for Groq, Gemini, and other providers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        groq_key = st.text_input("Groq API Key", type="password", placeholder="Enter your Groq Key")
        st.info("Status: ACTIVE" if groq_key.strip() else "Status: NOT SET")
    
    with col2:
        gemini_key = st.text_input("Gemini API Key", type="password", placeholder="Enter your Gemini Key", value=st.session_state['settings'].get('api_key', ''))

    if st.button("Save API Configuration", type="primary"):
        st.session_state['settings']['api_key'] = gemini_key
        st.success("API Keys saved successfully!")

# Appearance Section
st.write("## ")
with st.container():
    st.markdown("""
    <div class="glass-card">
        <h3>🎨 System Interface</h3>
        <p style="opacity: 0.6; font-size: 0.9rem;">Personalize the theme and visual density of your workspace.</p>
    </div>
    """, unsafe_allow_html=True)
    
    theme = st.selectbox("Interface Theme", ["Nexus Noir (Dark)", "Arctic Light (Coming Soon)"], index=0)
    glass_opacity = st.slider("Glass Transparency", 0.0, 1.0, 0.05)
    
    if st.button("Apply UI Changes"):
        st.toast("Appearance updated!")

# Session Management
st.write("## ")
if st.button("🗑️ Reset All Data", help="Permanently clear session data and history"):
    st.session_state.clear()
    st.rerun()