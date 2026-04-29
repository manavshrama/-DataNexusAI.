import streamlit as st
from modules.data_loader import DataLoader
from utils.auth import logout

def render_sidebar():
    """Render the sidebar with logo, API configuration, file info, and logout."""
    with st.sidebar:
        # Logo and Branding
        st.markdown('<div style="text-align: center; padding-bottom: 20px;">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=100)
        st.markdown('<h1 class="gradient-text" style="font-size: 1.8rem; margin-bottom: 0;">NEXUS AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 0.7rem; color: #00D2FF; letter-spacing: 0.3em; margin-top: -5px; font-weight: 700;">COMMAND CENTER</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('---')
        
        # API Configuration
        st.subheader("🔑 API Configuration")
        st.session_state.groq_key = st.text_input("Groq API Key", value=st.session_state.get('groq_key', ''), type="password")
        st.session_state.gemini_key = st.text_input("Gemini API Key", value=st.session_state.get('gemini_key', ''), type="password")
        
        # File/Data Info
        if st.session_state.get('df') is not None:
            st.markdown("---")
            st.subheader("📊 Dataset Stats")
            st.caption(f"**Name:** {st.session_state.get('file_name', 'Unnamed Dataset')}")
            stats = DataLoader.get_stats(st.session_state.df)
            st.caption(f"**Rows:** {stats['rows']:,}")
            st.caption(f"**Cols:** {stats['cols']:,}")
            
            if st.button("Reset All Data", use_container_width=True):
                st.session_state.df = st.session_state.df_original.copy()
                st.rerun()
        else:
            st.info("No data loaded. Visit Upload tab.")
        
        st.markdown("---")
        # App Info and Logout
        if st.button("🔓 Sign Out", use_container_width=True):
            logout()
            
        st.caption("v1.2.3 | Nexus System Core")
