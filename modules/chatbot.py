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
        self.system_prompt = """
        You are Data Nexus AI, a expert data scientist. 
        ALWAYS respond in pure valid JSON only. Never use plain text outside JSON.
        
        JSON Schema:
        {
          "answer": "Markdown analysis string",
          "insight_type": "analysis | chart | query | summary | ml_suggestion | error",
          "chart": {
            "type": "bar | line | scatter | pie | histogram | box | area | heatmap",
            "x": "column name",
            "y": "column name",
            "color": "column name or null",
            "title": "Chart title",
            "agg": "sum | mean | count | max | min | null"
          },
          "query_filter": "pandas query string or null",
          "key_metrics": [{"label": "Name", "value": "val", "delta": "diff"}],
          "suggestions": ["suggestion 1", "suggestion 2"],
          "confidence": "high | medium | low"
        }
        """

    def get_dataset_summary(self, df):
        summary = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "stats": df.describe().to_dict(),
            "sample": df.head(5).to_dict()
        }
        return json.dumps(summary)

    def ask(self, query, df, history):
        prompt = f"Context: Dataset Summary: {self.get_dataset_summary(df)}\n"
        prompt += f"Chat History: {json.dumps(history[-6:])}\n"
        prompt += f"User Question: {query}"
        
        # Try Groq first
        if self.groq_key:
            try:
                client = Groq(api_key=self.groq_key)
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-8b-8192",
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                st.warning(f"Groq failed, falling back to Gemini... ({str(e)})")
        
        # Fallback to Gemini
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash', 
                                              generation_config={"response_mime_type": "application/json"})
                res = model.generate_content([self.system_prompt, prompt])
                return json.loads(res.text)
            except Exception as e:
                return {"answer": f"API Error: Both providers failed. {str(e)}", "insight_type": "error", "suggestions": [], "confidence": "low"}
        
        return {"answer": "No API keys provided.", "insight_type": "error", "suggestions": [], "confidence": "low"}
