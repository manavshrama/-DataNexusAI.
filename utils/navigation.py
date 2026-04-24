import streamlit as st
from modules.data_loader import DataLoader
from utils.auth import logout

def render_unified_sidebar(default_index=0):
    """
    Renders the custom features (API Keys, Data Stats) into the sidebar.
    Note: We are letting Streamlit handle the native page navigation for a cleaner experience.
    """
    with st.sidebar:
        # Branding
        st.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=60)
        st.markdown('<h2 class="gradient-text">DataNexus AI</h2>', unsafe_allow_html=True)
        st.markdown('---')
        
        # --- ORIGINAL FEATURES (API & DATA) ---
        
        # API Configuration (Restored to prominent position)
        st.subheader("🔑 API Configuration")
        st.session_state.groq_key = st.text_input("Groq API Key", value=st.session_state.get('groq_key', ''), type="password")
        st.session_state.gemini_key = st.text_input("Gemini API Key", value=st.session_state.get('gemini_key', ''), type="password")
        
        # Active Data Stats (Restored to prominent position)
        if st.session_state.get('df') is not None:
            st.markdown("---")
            st.subheader("📊 Active Dataset")
            st.caption(f"**Source:** {st.session_state.get('file_name', 'Unknown')}")
            stats = DataLoader.get_stats(st.session_state.df)
            st.caption(f"**Rows:** {stats['rows']:,} | **Cols:** {stats['cols']}")
            if st.button("Reset All Data", use_container_width=True):
                st.session_state.df = st.session_state.df_original.copy()
                st.rerun()
        
        st.markdown("---")
        # Logout
        if st.button("🔓 Sign Out", use_container_width=True):
            logout()
            
        st.caption("v1.2.2 | Nexus System Core")
        st.markdown('---')
        st.markdown('<div style="text-align: center; opacity: 0.5; font-size: 0.8rem;">Select a page below:</div>', unsafe_allow_html=True)
