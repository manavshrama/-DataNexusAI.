import json
import pandas as pd
import streamlit as st
from groq import Groq
import google.generativeai as genai
from typing import Optional, List, Dict, Any

class ChatbotModule:
    """AI Data Analyst Chatbot with Groq-to-Gemini fallback and structured JSON output."""
    
    def __init__(self, groq_key: Optional[str] = None, gemini_key: Optional[str] = None):
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
        - OUTPUT ONLY VALID JSON. NO PREAMBLE. NO COMMENTARY.
        - LIMIT "answer" field to max 3 punchy, technical sentences or bullet points.
        - ALWAYS wrap Python code in ```python blocks.
        - PREFER Plotly: `import plotly.express as px`. Use `st.plotly_chart(fig, use_container_width=True)`.
        - Assume 'df' is available.
        
        ### RESPONSE SCHEMA (JSON ONLY):
        {
          "answer": "Strictly technical & concise (max 50 words)",
          "insight_type": "analysis | chart | query | summary | error",
          "python_code": "The full pandas/plotly code to execute",
          "suggestions": ["step 1", "step 2"],
          "confidence": "high | medium | low"
        }
        """

    def get_dataset_summary(self, df: Optional[pd.DataFrame]) -> Dict[str, Any]:
        """Generates a compressed Semantic Schema to minimize token usage."""
        if df is None: return {"status": "No dataset loaded."}
        
        schema = {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "fields": []
        }
        
        for col in df.columns:
            col_info = {
                "name": col,
                "type": str(df[col].dtype),
                "nulls": int(df[col].isnull().sum())
            }
            
            # Add range for numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info["range"] = [float(df[col].min()), float(df[col].max())]
            # Add unique samples for categorical
            else:
                uniques = df[col].unique()
                col_info["unique_count"] = len(uniques)
                col_info["samples"] = list(uniques[:3])
            
            schema["fields"].append(col_info)
            
        return schema

    def _local_fallback(self, query: str, df: Optional[pd.DataFrame]) -> Dict[str, Any]:
        """Generate a simple fallback response when no AI APIs are configured.

        Handles basic queries about the dataset.
        """
        if df is None:
            return {
                "answer": "No dataset loaded. Please upload a CSV file.",
                "insight_type": "error",
                "python_code": "",
                "suggestions": [],
                "confidence": "low",
            }
        q = query.lower()
        # Simple heuristic responses
        if "columns" in q:
            cols = list(df.columns)
            answer = f"Dataset columns are: {', '.join(cols)}."
            code = "st.write(df.columns)"
        elif "head" in q or "preview" in q:
            answer = "Here are the first few rows of the dataset."
            code = "st.dataframe(df.head())"
        elif "summary" in q or "stat" in q:
            answer = "Statistical summary of numeric columns."
            code = "st.write(df.describe())"
        else:
            answer = "I can provide basic data insights. Try asking about columns, preview, or summary."
            code = ""
        return {
            "answer": answer,
            "insight_type": "summary",
            "python_code": code,
            "suggestions": [],
            "confidence": "medium",
        }

    def ask(self, query: str, df: Optional[pd.DataFrame], history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Processes a user query using the available AI engines with optimized context.
        Falls back to a local heuristic if no API keys are configured.
        """
        # Build Semantic Knowledge Base Context (Aggressive Pruning)
        summary = self.get_dataset_summary(df)
        knowledge_context = f"SEMANTIC_SCHEMA: {json.dumps(summary, default=str)}\n"
        
        prompt = f"{knowledge_context}\nCHAT_HISTORY: {json.dumps(history[-5:], default=str)}\nUSER_QUERY: {query}"
        
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
            except json.JSONDecodeError:
                st.error("Error: Received malformed JSON from Groq Engine.")
            except Exception as e:
                st.warning(f"Groq Engine Offline: {e}")
        
        # Priority 2: Gemini
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                res = model.generate_content(
                    f"{self.system_prompt}\n\n{prompt}",
                    generation_config={"response_mime_type": "application/json"}
                )
                return json.loads(res.text)
            except json.JSONDecodeError:
                st.error("Error: Received malformed JSON from Gemini Engine.")
            except Exception as e:
                st.error(f"Gemini Engine Offline: {e}")
        
        # Fallback: local heuristic response
        return self._local_fallback(query, df)
