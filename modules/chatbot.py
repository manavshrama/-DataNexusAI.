import json
import pandas as pd
import streamlit as st
from groq import Groq
import google.generativeai as genai

class ChatbotModule:
    """AI Data Analyst Chatbot with Groq-to-Gemini fallback and structured JSON output."""
    
    def __init__(self, groq_key=None, gemini_key=None):
        self.groq_key = groq_key
        self.gemini_key = gemini_key
        # --- GRAFTED SYSTEM PROMPT (DataNexus Visual Engine v2) ---
        self.system_prompt = """
        ### IDENTITY: DataNexus AI Visual Engine
        ### MISSION: Deliver high-precision code and deep statistical insights for any CSV data.
        
        ### KNOWLEDGE BASE PROTOCOL:
        1. EDA: summary stats, missing value detection, outlier filtering (IQR), correlation analysis.
        2. DATA TRANSFORMATIONS: pd.melt, pd.pivot, grouping, filtering, date parsing.
        
        ### VISUAL UNIVERSE (30+ CHART TYPES SUPPORTED):
        - Distribution: Histogram, KDE Plot, Box Plot, Violin Plot, Strip Plot, Rug Plot, Ridge Plot.
        - Comparison: Bar (Grouped/Stacked), Horizontal Bar, Lollipop, Dumbbell, Bullet Chart.
        - Relationship: Scatter, Bubble, 3D Scatter, Pair Plot, Heatmap, Density Heatmap, Joint Plot.
        - Composition: Pie, Donut, Sunburst, Treemap, Waterfall, Waffle Chart, Stacked Area.
        - Time Series: Line Chart, Area Chart, Candlestick, OHLC, Step Chart.
        - Advanced: Sankey Diagram, Funnel Chart, Parallel Coordinates, Radar/Spider Chart, Choropleth Map.
        
        ### EXECUTION RULES:
        - ALWAYS wrap Python code in ```python blocks.
        - PREFER Plotly: `import plotly.express as px`. Use `st.plotly_chart(fig, use_container_width=True)`.
        - USE Seaborn/Matplotlib for complex stats: `fig, ax = plt.subplots()`, then `st.pyplot(fig)`.
        - Assume 'df' is available in the environment.
        
        ### RESPONSE SCHEMA (JSON ONLY):
        {
          "answer": "Professional analysis and findings",
          "insight_type": "analysis | chart | query | summary | error",
          "python_code": "The full pandas/plotly code to execute",
          "suggestions": ["next step 1", "next step 2"],
          "confidence": "high | medium | low"
        }
        """

    def get_dataset_summary(self, df):
        if df is None: return "No dataset."
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "nulls": df.isnull().sum().to_dict(),
            "head": df.head(3).to_dict()
        }

    def ask(self, query, df, history):
        # Build Knowledge Base Context
        summary = self.get_dataset_summary(df)
        knowledge_context = f"DATASET_KNOWLEDGE_BASE: {json.dumps(summary)}\n"
        
        prompt = f"{knowledge_context}\nCHAT_HISTORY: {json.dumps(history[-5:])}\nUSER_QUERY: {query}"
        
        # Priority 1: Groq
        if self.groq_key:
            try:
                client = Groq(api_key=self.groq_key)
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-70b-8192",
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                st.warning(f"Groq Engine Offline: {e}")
        
        # Priority 2: Gemini
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                # For Gemini, we merge system and user for best performance in JSON mode
                res = model.generate_content(
                    f"{self.system_prompt}\n\n{prompt}",
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(res.text)
            except Exception as e:
                st.error(f"Gemini Engine Offline: {e}")
        
        return {"answer": "Error: AI Engines are disconnected. Please verify API keys in the sidebar.", "insight_type": "error"}
