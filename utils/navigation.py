import streamlit as st
from streamlit_option_menu import option_menu

def sidebar_nav(default_index=0):
    """Common sidebar navigation for all pages."""
    with st.sidebar:
        st.markdown('<h1 class="gradient-text">DataNexusAI</h1>', unsafe_allow_html=True)
        # st.image("assets/logo.svg", width=120)  # Use actual asset if exists
        
        options = ["Home", "Dashboard", "Upload Data", "AI Chat", "ML Studio", "Results", "Settings"]
        icons = ["house", "speedometer2", "cloud-upload", "chat-dots", "cpu", "clipboard-data", "gear"]
        
        selected = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            default_index=default_index,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#00C9A7", "font-size": "18px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "5px", "border-radius": "8px", "--hover-color": "rgba(108, 99, 255, 0.1)"},
                "nav-link-selected": {"background-color": "rgba(108, 99, 255, 0.2)", "border-left": "3px solid #6C63FF", "color": "white"},
            }
        )
        
        # Navigation logic using st.switch_page (Native multi-page navigation)
        if selected != options[default_index]:
            if selected == "Home":
                st.switch_page("app.py")
            elif selected == "Dashboard":
                st.switch_page("pages/2_Dashboard.py")
            elif selected == "Upload Data":
                st.switch_page("pages/3_Upload.py")
            elif selected == "AI Chat":
                st.switch_page("pages/4_Chat.py")
            elif selected == "ML Studio":
                st.switch_page("pages/5_ML_Studio.py")
            elif selected == "Results":
                st.switch_page("pages/6_Results.py")
            elif selected == "Settings":
                st.switch_page("pages/7_Settings.py")
        
        st.markdown("---")
        st.caption("v1.0.0 | Nexus Labs")
        st.markdown("[GitHub](https://github.com) | [Support](https://example.com)")
    
    return selected
