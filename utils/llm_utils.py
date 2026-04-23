from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import streamlit as st

def get_chat_response(messages, api_key, dataset_summary="", data_snapshot=""):
    """Gets a response from OpenAI using LangChain.
    
    Args:
        messages: Chat history list of {"role": ..., "content": ...} dicts.
        api_key: OpenAI API key.
        dataset_summary: One-line metadata string (shape, dtypes, nulls, etc.).
        data_snapshot: Formatted string of df.head() and df.describe() for grounding.
    """
    if not api_key:
        return "⚠️ **API key not configured.** Go to **Settings** → set your OpenAI API key."
    
    chat = ChatOpenAI(openai_api_key=api_key, model="gpt-4-turbo-preview")
    
    # Build data snapshot section only when data is available
    snapshot_section = ""
    if data_snapshot:
        snapshot_section = f"""

### DATA SNAPSHOT (first 5 rows + descriptive statistics):
{data_snapshot}
"""

    system_prompt = f"""### ROLE: AI Chat / Data Science Engine
### GOAL: Execute technical data tasks on uploaded CSV/Excel files with maximum precision, rigor, and minimal prose.

### ACTIVE DATASET CONTEXT:
{dataset_summary}
{snapshot_section}

### TASK SCOPE:
1. **EDA**: Deliver concise summary statistics, correlation insights, distribution patterns, and key observations.
2. **Cleaning**: Detect nulls, duplicates, and outliers. Provide transformation code.
3. **Visualization**: When asked for charts, generate Python code using `matplotlib.pyplot`, `seaborn`, or `plotly`. Use `st.pyplot(fig)` or `st.plotly_chart(fig)` to render them.
4. **File Generation**: When asked to generate a file (e.g., cleaned data), provide the code to create a downloadable buffer and use `st.download_button`.

### OUTPUT RULES:
- **Accuracy First**: Never hallucinate data points.
- **Directness**: Strictly technical and actionable.
- **Code Blocks**: Always provide runnable Python code for any data manipulation or visualization.
- **Formatting**: Use Markdown tables for statistics.
- **Execution Context**: Assume `df` is already loaded in the environment as a pandas DataFrame.

### VISUALIZATION GUIDELINES:
- Use `import matplotlib.pyplot as plt` or `import plotly.express as px`.
- For Matplotlib: Always create a figure object `fig, ax = plt.subplots()` and end with `st.pyplot(fig)`.
- For Plotly: End with `st.plotly_chart(fig)`.

### FILE GENERATION GUIDELINES:
- To provide a download, use this pattern:
```python
import io
buffer = io.BytesIO()
df_processed.to_csv(buffer, index=False)
st.download_button(label="Download Processed Data", data=buf.getvalue(), file_name="cleaned_data.csv", mime="text/csv")
```

### CONTEXT:
User is working in a Python-based Data Science Dashboard (Streamlit). Responses must be highly technical and contain EXECUTION-READY code blocks."""
    
    langchain_messages = [SystemMessage(content=system_prompt)]
    for msg in messages:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        else:
            langchain_messages.append(AIMessage(content=msg["content"]))
            
    try:
        response = chat.invoke(langchain_messages)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"
