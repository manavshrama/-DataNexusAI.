import streamlit as st

def load_css():
    """Injects the comprehensive NexusNoir CSS from constants."""
    from utils.constants import CUSTOM_CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_hero(title, subtitle, icon="🔮"):
    """Renders a cinematic Hero section with neon gradients."""
    st.markdown(f"""
    <div style="padding: 2rem 0; text-align: left;">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
            <span style="font-size: 40px;">{icon}</span>
            <h1 class="gradient-text" style="font-size: 3.5rem; margin: 0; line-height: 1;">{title}</h1>
        </div>
        <p style="font-family: 'Outfit', sans-serif; font-size: 1.2rem; color: rgba(255,255,255,0.6); font-weight: 300; margin-left: 55px;">
            {subtitle}
        </p>
    </div>
    <hr style="border: 0; height: 1px; background: linear-gradient(90deg, rgba(0,210,255,0.5), transparent); margin-bottom: 2rem;">
    """, unsafe_allow_html=True)

def glass_card(title=None, subtitle=None):
    """Context manager for glass cards."""
    header_html = ""
    if title:
        header_html += f'<h3 style="margin-top: 0; margin-bottom: 5px;">{title}</h3>'
    if subtitle:
        header_html += f'<p style="color: rgba(255,255,255,0.5); font-size: 0.9rem; margin-bottom: 20px;">{subtitle}</p>'
    
    if header_html:
        st.markdown(header_html, unsafe_allow_html=True)
    
    return st.container(border=True)
