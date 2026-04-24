import streamlit as st

def load_css():
    """Injects custom CSS for High-End Glassmorphism 2.0 — Premium SaaS Edition."""
    nexus_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@400;500;700&display=swap');

    :root {
        --bg-primary: #0D0D1A;
        --bg-secondary: #12122A;
        --glass-surface: rgba(255, 255, 255, 0.04);
        --glass-border: rgba(255, 255, 255, 0.08);
        --accent-purple: #7B5EA7;
        --accent-teal: #00C9A7;
        --text-primary: #FFFFFF;
        --text-muted: #A0A0CC;
        --success: #00C9A7;
        --danger: #FF4C6A;
        --card-shadow: 0 4px 32px rgba(0, 0, 0, 0.3);
        --hover-shadow: 0 0 24px rgba(123,94,167,0.4);
    }

    /* Global Foundation & Animated Background System */
    .stApp {
        background-color: var(--bg-primary);
        background-image: radial-gradient(circle at 30% 30%, #1A0D2E 0%, transparent 40%),
                          radial-gradient(circle at 70% 70%, #0D1A2E 0%, transparent 40%);
        background-attachment: fixed;
        background-size: 200% 200%;
        animation: gradientShift 10s ease infinite;
        color: var(--text-primary);
        font-family: 'DM Sans', sans-serif;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 700;
        color: var(--text-primary);
    }

    p, span, div, li, td, th {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-muted);
    }

    /* Floating Navigation Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 13, 26, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
    }
    
    /* Hide default sidebar content text color issues */
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: var(--text-muted) !important;
    }

    /* High-Refraction Glass Card */
    .glass-card {
        background: var(--glass-surface);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--hover-shadow);
    }

    .glass-card-title {
        font-family: 'Syne', sans-serif;
        font-size: 20px;
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .glass-card-subtitle {
        font-size: 14px;
        color: var(--text-muted);
        margin-bottom: 1rem;
        font-weight: 400;
    }

    /* Hero Section Component Styles */
    .hero-container {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--glass-border);
        animation: fadeInSlideUp 0.6s ease-out;
    }
    
    @keyframes fadeInSlideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .hero-title {
        font-size: 64px;
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-teal));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        line-height: 1.2;
        background-size: 200% auto;
        animation: textGradientShift 4s ease infinite;
    }
    
    @keyframes textGradientShift {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }

    .hero-subtitle {
        font-size: 18px;
        color: var(--text-muted);
        font-weight: 400;
        max-width: 800px;
    }

    /* Premium Gradient Text for Generic Use */
    .gradient-text {
        background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-teal) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* Nexus Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-teal)) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'DM Sans', sans-serif !important;
        letter-spacing: 0.5px !important;
        transition: all 0.1s ease !important;
        box-shadow: 0 4px 15px rgba(123, 94, 167, 0.3) !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.02) !important;
        filter: brightness(1.1) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    .stButton>button:active {
        transform: scale(0.97) !important;
    }

    /* Customizing Metric Widgets */
    div[data-testid="stMetric"] {
        background: var(--glass-surface);
        border: 1px solid var(--glass-border);
        padding: 1.2rem;
        border-radius: 16px;
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: var(--hover-shadow);
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 2.2rem !important;
        color: var(--text-primary) !important;
    }

    div[data-testid="stMetricDelta"] svg {
        fill: var(--accent-teal) !important;
    }
    
    div[data-testid="stMetricDelta"] div[data-testid="stMetricDeltaIcon-Down"] svg {
        fill: var(--danger) !important;
    }

    /* Chat Styling */
    .chat-bubble {
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(10px);
        margin-bottom: 12px;
        line-height: 1.6;
        font-size: 14px;
    }
    .user-bubble {
        background: rgba(123, 94, 167, 0.1) !important;
        border-right: 3px solid var(--accent-purple) !important;
        margin-left: 2rem;
        box-shadow: 0 0 15px rgba(123, 94, 167, 0.1);
    }
    .assistant-bubble {
        background: rgba(0, 201, 167, 0.05) !important;
        border-left: 3px solid var(--accent-teal) !important;
        margin-right: 2rem;
        box-shadow: 0 0 15px rgba(0, 201, 167, 0.1);
    }

    /* Form Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stSlider>div>div {
        background-color: var(--glass-surface) !important;
        border: 1px solid var(--glass-border) !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
    }
    
    /* DataFrame/Table styling override */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        overflow: hidden;
    }

    /* Hide Defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1.5rem; padding-bottom: 3rem; }

    /* Streamlit Tab Styling Overhaul */
    div[data-testid="stTabs"] {
        background: transparent !important;
    }
    
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        color: var(--text-muted) !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 20px 20px 0 0 !important;
    }

    button[data-baseweb="tab"]:hover {
        color: var(--text-primary) !important;
        background-color: var(--glass-surface) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--text-primary) !important;
        border-bottom: 2px solid var(--accent-teal) !important;
        background-color: rgba(0, 201, 167, 0.1) !important;
    }

    /* Loading Spinner */
    .stSpinner > div > div {
        border-color: var(--accent-teal) transparent transparent transparent !important;
    }

    /* Markdown elements inside st.chat_message */
    div[data-testid="stChatMessageContent"] pre {
        background-color: #0A0A15 !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
    }

    /* Drop Zone styling for Upload */
    div[data-testid="stFileUploader"] > section {
        background-color: var(--glass-surface) !important;
        border: 2px dashed var(--glass-border) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(12px) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stFileUploader"] > section:hover {
        border-color: var(--accent-purple) !important;
        box-shadow: 0 0 20px rgba(123,94,167,0.2) !important;
    }

    </style>
    """
    st.markdown(nexus_css, unsafe_allow_html=True)

def render_hero(title, subtitle, cta_label=None):
    """Renders a premium Hero section for each tab/page."""
    cta_html = f"""<div style="margin-top: 1rem;"><button style="background: linear-gradient(135deg, #7B5EA7, #00C9A7); color: white; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; padding: 0.6rem 1.5rem; font-weight: 600; cursor: pointer; font-family: 'DM Sans', sans-serif;">{cta_label}</button></div>""" if cta_label else ""
    st.markdown(f"""
    <div class="hero-container">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
        {cta_html}
    </div>
    """, unsafe_allow_html=True)

def glass_card(content, title=None, subtitle=None):
    """Helper to wrap content in a premium glass card."""
    title_html = f'<div class="glass-card-title">{title}</div>' if title else ""
    subtitle_html = f'<div class="glass-card-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="glass-card">
        {title_html}
        {subtitle_html}
        {content}
    </div>
    """, unsafe_allow_html=True)

