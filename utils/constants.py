# --- CUSTOM CSS ---
CUSTOM_CSS = """
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

    /* Gradient Text Utility */
    .gradient-text {
        background: linear-gradient(90deg, #00D2FF, #9D50BB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Syne', sans-serif;
        font-weight: 800;
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
