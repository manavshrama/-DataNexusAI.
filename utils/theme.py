import streamlit as st

def load_css():
    """Injects minimal custom CSS to ensure visibility."""
    st.markdown("""
    <style>
    /* Ensure Sidebar and Main Menu are visible */
    section[data-testid="stSidebar"] {
        visibility: visible !important;
        display: block !important;
    }
    #MainMenu {
        visibility: visible !important;
    }
    header {
        visibility: visible !important;
    }
    
    /* Basic Glassmorphism for the cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    .gradient-text {
        background: linear-gradient(45deg, #7B5EA7, #00C9A7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def render_hero(title, subtitle, cta_label=None):
    """Renders a simple Hero section."""
    st.markdown(f"## {title}")
    st.markdown(f"*{subtitle}*")
    st.markdown("---")

def glass_card(content, title=None, subtitle=None):
    """Simple glass card wrapper."""
    with st.container():
        if title: st.subheader(title)
        if subtitle: st.caption(subtitle)
        st.write(content)
