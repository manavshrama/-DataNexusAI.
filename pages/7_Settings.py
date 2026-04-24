import streamlit as st
from utils.theme import load_css, glass_card, render_hero
from components.sidebar_ui import render_sidebar

st.set_page_config(page_title="DataNexusAI - Settings", page_icon="⚙️", layout="wide")
load_css()
render_sidebar()

render_hero("Control Center", "Configure your API keys, preferences, and workspace options")

# ── API Integration Center ──────────────────────────────────────────────
st.markdown("### 🔑 Intelligence Keys")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        groq_key = st.text_input("Groq Cloud Key", type="password", placeholder="gsk_...")
        st.caption("Status: " + ("🟢 Connected" if groq_key else "🔴 Offline"))
    
    with col2:
        gemini_key = st.text_input("Gemini Pro Key", type="password", placeholder="AIza...", value=st.session_state.get('settings', {}).get('api_key', ''))
        st.caption("Status: " + ("🟢 Connected" if gemini_key else "🔴 Offline"))

    if st.button("Save Security Config", use_container_width=True):
        if 'settings' not in st.session_state: st.session_state['settings'] = {}
        st.session_state['settings']['api_key'] = gemini_key
        st.success("Universal keys saved to session memory.")

# ── Performance & Aesthetics ───────────────────────────────────────────
st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
st.markdown("### 🎨 Visual Calibration")
with st.container():
    col_a, col_b = st.columns(2)
    with col_a:
        theme = st.selectbox("Interface Spectrum", ["Nexus Noir (Obsidian)", "Solar Flare (Light Mode - Soon)"], index=0)
        st.markdown('<p style="font-size:0.8rem; opacity:0.5;">Active: Obsidian High-Contrast</p>', unsafe_allow_html=True)
    with col_b:
        glass_opacity = st.slider("Glass Transparency Blur", 0.0, 1.0, 0.05)
        st.markdown(f'<p style="font-size:0.8rem; opacity:0.5;">Current: {int(glass_opacity*100)}% refraction</p>', unsafe_allow_html=True)
    
    if st.button("Synchronize Interface", use_container_width=True):
        st.toast("Nexus visual system re-calibrated.")

# ── Memory Management ──────────────────────────────────────────────────
st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
st.markdown("### ⚠️ Memory Purge")
with st.container():
    st.markdown('<p style="font-size:0.9rem; opacity:0.6;">Warning: This will disconnect all linked datasets and purge chat history from the current session.</p>', unsafe_allow_html=True)
    if st.button("🗑️ Reset All Neural Data", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.write("---")
st.markdown('<p style="text-align:center; opacity:0.3; font-size:0.8rem;">DataNexus AI | Secure Environment Protocol 1.2.0</p>', unsafe_allow_html=True)