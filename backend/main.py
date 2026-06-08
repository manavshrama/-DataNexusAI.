from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import uuid
from typing import Optional
from pydantic import BaseModel
from collections import OrderedDict

app = FastAPI(title="DataNexus AI backend")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store with size limit to prevent memory leaks
MAX_SESSIONS = 100
sessions: OrderedDict = OrderedDict()

class ChatRequest(BaseModel):
    message: str
    session_id: str
    dataset_name: Optional[str] = None

class Insight(BaseModel):
    title: str
    dataset: str
    severity: str
    summary: str
    time: str

@app.get("/")
async def root():
    return {"status": "Nexus Core Online", "version": "1.0.0"}

@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    content = await file.read()
    
    try:
        filename_lower = (file.filename or "").lower()
        if filename_lower.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif filename_lower.endswith(('.xlsx', '.xlsm', '.xltx', '.xltm', '.xls', '.xlsb', '.ods')):
            try:
                if filename_lower.endswith(('.xlsx', '.xlsm', '.xltx', '.xltm')):
                    df = pd.read_excel(io.BytesIO(content), engine='openpyxl')
                elif filename_lower.endswith('.xls'):
                    df = pd.read_excel(io.BytesIO(content), engine='xlrd')
                elif filename_lower.endswith('.xlsb'):
                    df = pd.read_excel(io.BytesIO(content), engine='pyxlsb')
                elif filename_lower.endswith('.ods'):
                    df = pd.read_excel(io.BytesIO(content), engine='odf')
            except Exception as engine_err:
                try:
                    df = pd.read_excel(io.BytesIO(content))
                except Exception as fallback_err:
                    raise engine_err
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file format: {file.filename}")
            
        # Evict oldest session if limit reached
        if len(sessions) >= MAX_SESSIONS:
            sessions.popitem(last=False)

        sessions[session_id] = {
            "df": df,
            "filename": file.filename
        }
        
        return {"session_id": session_id, "filename": file.filename, "rows": len(df), "cols": len(df.columns)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/{session_id}")
async def get_stats(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    df = sessions[session_id]["df"]
    return {
        "columns": list(df.columns),
        "shape": df.shape,
        "null_counts": df.isnull().sum().to_dict()
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    # This would call chatbot.py logic
    # Simplified for now
    response = f"AI Insight for {request.message} in {request.dataset_name}"
    return {"response": response}

@app.get("/insights")
async def fetch_insights():
    # Return mockup or real generated insights
    return [
        { 
          "id": 1, 
          "title": 'Revenue Anomaly Detected', 
          "dataset": 'sales_q3_report.csv', 
          "severity": 'high', 
          "summary": 'A 45% spike in sales was detected on Aug 15th.',
          "time": '2 hours ago'
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
