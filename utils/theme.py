import streamlit as st
import base64
import os

def get_base64_image(image_path):
    if not image_path or not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def load_css():
    """Injects the comprehensive NexusNoir CSS from constants."""
    from utils.constants import DARK_CSS, LIGHT_CSS
    theme = st.session_state.get('ui_theme', 'dark')
    css = DARK_CSS if theme == 'dark' else LIGHT_CSS
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_hero(title, subtitle, icon="🔮", bg_image=None):
    """Renders a cinematic Hero section with optional background image and neon gradients."""
    b64_img = get_base64_image(bg_image)
    bg_style = f"background: url('data:image/png;base64,{b64_img}'); background-size: cover; background-position: center;" if b64_img else "background: rgba(255,255,255,0.02);"
    
    st.markdown(f"""
    <div style="
        {bg_style}
        padding: 3rem 2rem; 
        border-radius: 20px; 
        margin-bottom: 2rem; 
        position: relative; 
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05);
    ">
        <div style="
            position: absolute; 
            top: 0; left: 0; right: 0; bottom: 0; 
            background: linear-gradient(90deg, #050505 30%, transparent 100%);
            z-index: 1;
        "></div>
        <div style="position: relative; z-index: 2; display: flex; align-items: center; gap: 20px;">
            <span style="font-size: 50px; filter: drop-shadow(0 0 10px rgba(0,210,255,0.5));">{icon}</span>
            <div>
                <h1 class="gradient-text" style="font-size: 3.8rem; margin: 0; line-height: 1.1; letter-spacing: -0.05em;">{title}</h1>
                <p style="font-family: 'Outfit', sans-serif; font-size: 1.3rem; color: rgba(255,255,255,0.7); font-weight: 300; margin-top: 10px; margin-bottom: 0;">
                    {subtitle}
                </p>
            </div>
        </div>
    </div>
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
    
def load_lottie_url(url: str):
    import requests
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def render_lottie(url, height=200, key=None):
    from streamlit_lottie import st_lottie
    lottie_json = load_lottie_url(url)
    if lottie_json:
        st_lottie(lottie_json, height=height, key=key)
