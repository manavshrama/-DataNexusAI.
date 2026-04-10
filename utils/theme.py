import streamlit as st

def load_css():
    """Injects custom CSS for glassmorphism and premium styling."""
    glass_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Poppins:wght@500;700&display=swap');

    :root {
        --primary-color: #6C63FF;
        --secondary-color: #00C9A7;
        --accent-color: #845EC2;
        --bg-dark: #0F0F1A;
        --bg-gradient: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.12);
        --text-color: #FFFFFF;
        --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* Global Styles */
    .stApp {
        background: var(--bg-gradient);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }

    /* Glass Card Style */
    .glass-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        margin-bottom: 1rem;
    }

    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Customizing Streamlit Elements */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.5);
        border: none;
        color: white;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 15, 26, 0.95);
        border-right: 1px solid var(--glass-border);
    }

    /* Metric Styling */
    div[data-testid="stMetricValue"] {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #FFF, #CCC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid var(--glass-border) !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* Hide Streamlit Header/Footer for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Step Badge */
    .step-badge {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-right: 12px;
        box-shadow: 0 4px 10px rgba(108, 99, 255, 0.3);
        font-size: 0.9rem;
    }

    /* Prediction Result Card */
    .prediction-card {
        text-align: center;
        padding: 2.5rem;
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.03);
    }

    /* Animations */
    @keyframes shine {
        from { background-position: 0% center; }
        to { background-position: 200% center; }
    }

    .shimmer-text {
        background: linear-gradient(to right, var(--primary-color) 0%, var(--secondary-color) 50%, var(--primary-color) 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        font-weight: 700;
    }

    @keyframes shimmer-bg {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .shimmer-card {
        background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.03) 50%, rgba(255,255,255,0) 100%), var(--glass-bg);
        background-size: 200% 100%;
        animation: shimmer-bg 5s infinite;
    }

    /* Premium Chat Bubbles */
    .chat-bubble {
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(12px);
        box-shadow: var(--card-shadow);
        margin-bottom: 8px;
    }
    .user-bubble {
        background: rgba(108, 99, 255, 0.12) !important;
        border-right: 4px solid var(--primary-color) !important;
    }
    .assistant-bubble {
        background: rgba(0, 201, 167, 0.12) !important;
        border-left: 4px solid var(--secondary-color) !important;
    }

    </style>
    """
    st.markdown(glass_css, unsafe_allow_html=True)

def glass_card(content, title=None):
    """Helper to wrap content in a glass card."""
    if title:
        st.markdown(f'<div class="glass-card"><h3>{title}</h3>{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="glass-card">{content}</div>', unsafe_allow_html=True)
