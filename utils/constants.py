# --- CUSTOM CSS ---
DARK_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif !important;
        background-color: #050505 !important;
        color: #E0E0E0 !important;
    }
    
    /* Headers with Syne */
    h1, h2, h3, [data-testid="stHeader"] {
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.04em !important;
        text-transform: uppercase;
    }
    
    /* Sidebar Styling - Deep Obsidian */
    [data-testid="stSidebar"] {
        background-color: #0A0A0A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Premium Glass Cards */
    .stMetric, .stChatMessage, .stExpander, div.glass-card {
        background: rgba(20, 20, 20, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .stMetric:hover, .stExpander:hover {
        border-color: rgba(0, 210, 255, 0.3) !important;
        transform: translateY(-2px);
    }
    
    /* Cyber Gradient Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #9D50BB 0%, #6E48AA 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        font-family: 'Syne', sans-serif !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 15px rgba(157, 80, 187, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(157, 80, 187, 0.6) !important;
        background: linear-gradient(135deg, #00D2FF 0%, #3a7bd5 100%) !important;
    }
    
    /* Tabs - Minimalist & Sharp */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px !important;
        background-color: transparent !important;
        padding: 10px 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-radius: 10px !important;
        color: rgba(255, 255, 255, 0.4) !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 210, 255, 0.1) !important;
        color: #00D2FF !important;
        border-color: #00D2FF !important;
    }

    /* Chat Bubbles - Floating Glass */
    .user-bubble {
        background: rgba(0, 210, 255, 0.1) !important;
        border: 1px solid rgba(0, 210, 255, 0.2) !important;
        border-radius: 20px 20px 0 20px !important;
        padding: 15px 20px !important;
        margin: 15px 0 !important;
        float: right;
        clear: both;
        max-width: 80%;
    }
    .ai-bubble {
        background: rgba(157, 80, 187, 0.1) !important;
        border: 1px solid rgba(157, 80, 187, 0.2) !important;
        border-radius: 20px 20px 20px 0 !important;
        padding: 15px 20px !important;
        margin: 15px 0 !important;
        float: left;
        clear: both;
        max-width: 80%;
    }

    /* Grain Overlay for Texture */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url("https://grainy-gradients.vercel.app/noise.svg");
        opacity: 0.05;
        pointer-events: none;
        z-index: 9999;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        background: #050505;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00D2FF 0%, #9D50BB 100%);
        border-radius: 10px;
    }

    /* Status Indicator Animation */
    @keyframes pulse-dot {
        0% { transform: scale(0.9); opacity: 0.7; }
        50% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.7; }
    }
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: #00D2FF;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 10px #00D2FF;
        animation: pulse-dot 2s infinite ease-in-out;
    }

    /* Gradient Text Animation */
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .gradient-text {
        background: linear-gradient(-45deg, #00D2FF, #9D50BB, #00D2FF, #9D50BB);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Syne', sans-serif;
        font-weight: 800;
    }
</style>
"""
LIGHT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap');
    
    html, body, [data-testid=\"stAppViewContainer\"] {
        font-family: 'Outfit', sans-serif !important;
        background-color: #f7f7f7 !important;
        color: #202020 !important;
    }
    
    /* Headers with Syne */
    h1, h2, h3, [data-testid=\"stHeader\"] {
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        color: #111111 !important;
        letter-spacing: -0.04em !important;
        text-transform: uppercase;
    }
    
    /* Sidebar Light */
    [data-testid=\"stSidebar\"] {
        background-color: #ffffff !important;
        border-right: 1px solid rgba(0,0,0,0.05) !important;
    }
    
    /* Glass Cards Light */
    .stMetric, .stChatMessage, .stExpander, div.glass-card {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6E48AA 0%, #9D50BB 100%) !important;
    }
</style>
"""

# --- UI STRINGS ---
PAGE_TITLE = "Data Nexus AI"
PAGE_ICON = "🔮"
APP_HEADER = "🌌 DataNexus AI: Intelligent Command Center"
AI_ANALYST_TITLE = "💬 AI Data Analyst"
ML_LAB_TITLE = "🤖 Machine Learning Lab"
VIZ_STUDIO_TITLE = "Data Visualization Studio"
EDA_TITLE = "Exploratory Data Analysis"
EXPORT_TITLE = "Export Cleaned Data"
UPLOAD_TITLE = "Step 1: Upload & Initial stats"
