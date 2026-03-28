# --- CUSTOM CSS ---
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #0f0f1a;
        color: #e8e8f0;
    }
    
    /* Gradient Banner */
    .stAppHeader {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 5px;
    }
    
    h1, h2, h3 {
        font-weight: 700 !important;
        color: #fff !important;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1a1a2e;
        border-left: 5px solid #667eea;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Primary Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: transform 0.2s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
    }
    
    /* Chat Bubbles */
    .user-bubble {
        background-color: #764ba2;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 5px 0;
        float: right;
        clear: both;
        max-width: 80%;
    }
    .ai-bubble {
        background-color: #2a2a4a;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 5px 0;
        float: left;
        clear: both;
        max-width: 80%;
        border: 1px solid #667eea;
    }
</style>
"""

# --- UI STRINGS ---
PAGE_TITLE = "Data Nexus AI"
PAGE_ICON = "🔮"
APP_HEADER = "🔮 Data Science Hub"
AI_ANALYST_TITLE = "💬 AI Data Analyst"
ML_LAB_TITLE = "🤖 Machine Learning Lab"
VIZ_STUDIO_TITLE = "Data Visualization Studio"
EDA_TITLE = "Exploratory Data Analysis"
EXPORT_TITLE = "Export Cleaned Data"
UPLOAD_TITLE = "Step 1: Upload & Initial stats"
