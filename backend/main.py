from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Literal
import json
import os
from dotenv import load_dotenv

from utils import (
    convert_json_to_toon_util,
    convert_toon_to_json_util,
    query_data_with_gemini_util,
    check_api_keys,
    count_tokens
)

load_dotenv()

app = FastAPI(
    title="TOON Data & Token Studio API",
    description="API for JSON/TOON conversion and AI-powered data queries",
    version="1.0.0"
)

# CORS middleware - allows React frontend from any origin
# For production, update allow_origins with your specific Vercel domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your Vercel domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class JsonToToonRequest(BaseModel):
    json_input: str
    indent: int = 2
    delimiter: str = ","

class JsonToToonResponse(BaseModel):
    output: str
    json_data_tokens: int
    toon_data_tokens: int
    savings: int
    savings_percent: float
    # Backward compatibility if needed, but better to be clean
    json_tokens: int
    toon_tokens: int

class ToonToJsonRequest(BaseModel):
    toon_input: str

class ToonToJsonResponse(BaseModel):
    output: str
    toon_data_tokens: int
    json_data_tokens: int
    # Backward compatibility
    toon_tokens: int
    json_tokens: int

class QueryRequest(BaseModel):
    data_text: str
    question: str
    data_format: Literal["JSON", "TOON"]

class QueryResponse(BaseModel):
    answer: str
    prompt_tokens: int
    completion_tokens: int
    total_llm_tokens: int
    breakdown: dict
    data_format: str
    json_data_tokens: int
    toon_data_tokens: int
    data_savings_tokens: int
    data_savings_percent: float
    conversion_status: str
    exec_ms: float

class StatusResponse(BaseModel):
    langsmith_connected: bool
    gemini_configured: bool

class CountRequest(BaseModel):
    text: str

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "TOON Data & Token Studio API", "version": "1.0.0"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/status", response_model=StatusResponse)
def get_status():
    """Check API key configuration status"""
    status = check_api_keys()
    return status

@app.post("/api/convert/json-to-toon", response_model=JsonToToonResponse)
def json_to_toon(request: JsonToToonRequest):
    """Convert JSON to TOON format"""
    try:
        result = convert_json_to_toon_util(
            request.json_input, 
            request.indent, 
            request.delimiter
        )
        return result
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/convert/toon-to-json", response_model=ToonToJsonResponse)
def toon_to_json(request: ToonToJsonRequest):
    """Convert TOON to JSON format"""
    try:
        result = convert_toon_to_json_util(request.toon_input)
        return result
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/query", response_model=QueryResponse)
def query_data(request: QueryRequest):
    """Query data using Gemini AI"""
    try:
        result = query_data_with_gemini_util(
            request.data_text,
            request.question,
            request.data_format
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/count")
def count_text_tokens(request: CountRequest):
    count = count_tokens(request.text)
    return {"count": count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
