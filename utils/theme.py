import streamlit as st

def load_css():
    """Injects custom CSS for high-end Cosmic Glassmorphism and Premium UI."""
    nexus_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@400;600;800&display=swap');

    :root {
        --primary-color: #6C63FF;
        --secondary-color: #00C9A7;
        --accent-color: #845EC2;
        --bg-dark: #0A0A12;
        --bg-gradient: radial-gradient(circle at 50% 50%, #1A1A2E 0%, #0A0A12 100%);
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.1);
        --glass-highlight: rgba(255, 255, 255, 0.05);
        --text-primary: #FFFFFF;
        --text-secondary: rgba(255, 255, 255, 0.7);
        --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Global Foundation */
    .stApp {
        background: var(--bg-gradient);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    /* Floating Navigation Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 18, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
    }

    /* High-Refraction Glass Card */
    .glass-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 1.8rem;
        box-shadow: var(--card-shadow);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(108, 99, 255, 0.4);
        box-shadow: 0 12px 40px 0 rgba(108, 99, 255, 0.2);
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, var(--glass-highlight), transparent);
        transition: 0.5s;
    }

    .glass-card:hover::before {
        left: 100%;
    }

    /* Premium Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #6C63FF 0%, #00C9A7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
    }

    /* Nexus Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color)) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 25px rgba(108, 99, 255, 0.5) !important;
        border: none !important;
    }

    /* Customizing Metric Widgets */
    div[data-testid="stMetric"] {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.2rem !important;
        color: var(--secondary-color) !important;
    }

    /* Chat Styling */
    .chat-bubble {
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(10px);
        margin-bottom: 12px;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .user-bubble {
        background: rgba(108, 99, 255, 0.1) !important;
        border-right: 3px solid var(--primary-color) !important;
        margin-left: 2rem;
    }
    .assistant-bubble {
        background: rgba(0, 201, 167, 0.05) !important;
        border-left: 3px solid var(--secondary-color) !important;
        margin-right: 2rem;
    }

    /* Form Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stSlider>div>div {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid var(--glass-border) !important;
        color: white !important;
        border-radius: 12px !important;
    }

    /* Hide Defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }

    /* Streamlit Tab Styling Overhaul */
    div[data-testid="stTabs"] {
        background: transparent !important;
    }
    
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: var(--text-secondary) !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        border-bottom: 2px solid transparent !important;
    }

    button[data-baseweb="tab"]:hover {
        color: var(--text-primary) !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--primary-color) !important;
        border-bottom: 2px solid var(--primary-color) !important;
        background-color: rgba(108, 99, 255, 0.05) !important;
    }

    /* Shimmer Animation */
    @keyframes shimmer {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }
    .shimmer-text { animation: shimmer 2s infinite ease-in-out; }

    </style>
    """
    st.markdown(nexus_css, unsafe_allow_html=True)

def glass_card(content, title=None, subtitle=None):
    """Helper to wrap content in a premium glass card."""
    title_html = f'<h3 style="margin-bottom:0.2rem;">{title}</h3>' if title else ""
    subtitle_html = f'<p style="font-size:0.85rem; opacity:0.6; margin-bottom:1rem;">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    <div class="glass-card">
        {title_html}
        {subtitle_html}
        {content}
    </div>
    """, unsafe_allow_html=True)
