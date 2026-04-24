import streamlit as st
from streamlit_option_menu import option_menu
from modules.data_loader import DataLoader

def render_unified_sidebar(default_index=0):
    with st.sidebar:
        st.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=60)
        st.markdown('<h2 class="gradient-text">DataNexus AI</h2>', unsafe_allow_html=True)
        st.markdown('---')
        
        # GRAFT: Navigation Menu
        options = ["Home", "Dashboard", "Upload Data", "AI Chat", "ML Studio", "Results", "Settings"]
        icons = ["house", "speedometer2", "cloud-upload", "chat-dots", "cpu", "clipboard-data", "gear"]
        
        selected = option_menu(
            menu_title=None, options=options, icons=icons, default_index=default_index,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#00C9A7", "font-size": "18px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "5px", "border-radius": "8px"},
                "nav-link-selected": {"background-color": "rgba(108, 99, 255, 0.2)", "border-left": "3px solid #6C63FF", "color": "white"}
            }
        )
        
        st.markdown('---')
        
        # GRAFT: API & Settings
        with st.expander("🔑 API Configuration", expanded=False):
            st.session_state.groq_key = st.text_input("Groq API Key", value=st.session_state.get('groq_key', ''), type="password")
            st.session_state.gemini_key = st.text_input("Gemini API Key", value=st.session_state.get('gemini_key', ''), type="password")
        
        # GRAFT: Active Data Stats
        if st.session_state.get('df') is not None:
            with st.expander("📊 Active Nexus Data", expanded=True):
                st.caption(f"**Source:** {st.session_state.file_name}")
                stats = DataLoader.get_stats(st.session_state.df)
                st.caption(f"**Rows:** {stats['rows']:,} | **Cols:** {stats['cols']}")
                if st.button("Reset Data", use_container_width=True):
                    st.session_state.df = st.session_state.df_original.copy()
                    st.rerun()
        
        st.markdown("---")
        if st.button("🔓 Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

        st.caption("v1.2.0 | Nexus System Core")
        
        # GRAFT: Routing Logic
        if selected != options[default_index]:
            routing_map = {
                "Home": "streamlit_app.py",
                "Dashboard": "pages/2_Dashboard.py",
                "Upload Data": "pages/3_Upload.py",
                "AI Chat": "pages/4_Chat.py",
                "ML Studio": "pages/5_ML_Studio.py",
                "Results": "pages/6_Results.py",
                "Settings": "pages/7_Settings.py"
            }
            st.switch_page(routing_map[selected])
            
    return selected
