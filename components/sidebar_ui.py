import streamlit as st
from modules.data_loader import DataLoader

def render_sidebar():
    """Render the sidebar with logo, API configuration, and file info."""
    with st.sidebar:
        st.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=80)
        st.title("Data Nexus AI")
        st.markdown("---")
        
        st.subheader("🔑 API Configuration")
        st.session_state.groq_key = st.text_input("Groq API Key", value=st.session_state.groq_key, type="password")
        st.session_state.gemini_key = st.text_input("Gemini API Key", value=st.session_state.gemini_key, type="password")
        
        if st.session_state.df is not None:
            st.markdown("---")
            st.subheader("📊 File Info")
            st.write(f"**Name:** {st.session_state.file_name}")
            stats = DataLoader.get_stats(st.session_state.df)
            st.write(f"**Rows:** {stats['rows']:,}")
            st.write(f"**Cols:** {stats['cols']:,}")
            
            if st.button("Reset All Data"):
                st.session_state.df = st.session_state.df_original.copy()
                st.rerun()
