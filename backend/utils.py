import json
import time
import os
from dotenv import load_dotenv

import tiktoken
import toon_format as toon_encoder
import google.generativeai as genai
from langsmith import Client
from langsmith.run_helpers import traceable

# Load environment variables first
load_dotenv()

# Initialize Gemini Model (Cached single instance)
_temp_gemini_key = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = None

if _temp_gemini_key:
    try:
        genai.configure(api_key=_temp_gemini_key)
        GEMINI_MODEL = genai.GenerativeModel("gemini-2.5-flash")
    except Exception:
        pass

# Token counting using Gemini tokenizer
def count_tokens(text: str) -> int:
    """Count tokens using Gemini native tokenizer with tiktoken fallback"""
    try:
        if GEMINI_MODEL:
            return GEMINI_MODEL.count_tokens(text).total_tokens
    except Exception:
        pass  # Fall through to tiktoken fallback
    
    # Fallback to tiktoken
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

# API Key checks
def check_api_keys():
    """Check which API keys are configured"""
    langsmith_key = os.getenv("LANGSMITH_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    return {
        "langsmith_connected": bool(langsmith_key),
        "gemini_configured": bool(gemini_key)
    }

# Initialize LangSmith
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
langsmith_client = None
if LANGSMITH_API_KEY:
    langsmith_client = Client(api_key=LANGSMITH_API_KEY)
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY

# Initialize Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Conversion Functions
def convert_json_to_toon_util(json_input: str, indent: int, delimiter: str):
    """Convert JSON to TOON format with token tracking"""
    data = json.loads(json_input)
    toon_output = toon_encoder.encode(data, options={"indent": indent, "delimiter": delimiter})
    
    json_data_tokens = count_tokens(json_input)
    toon_data_tokens = count_tokens(toon_output)
    savings = json_data_tokens - toon_data_tokens
    savings_percent = (savings / json_data_tokens) * 100 if json_data_tokens > 0 else 0
    
    return {
        "output": toon_output,
        "json_data_tokens": json_data_tokens,
        "toon_data_tokens": toon_data_tokens,
        "savings": savings,
        "savings_percent": savings_percent
    }

def convert_toon_to_json_util(toon_input: str):
    """Convert TOON to JSON format with token tracking"""
    try:
        json_output = toon_encoder.decode(toon_input)
        json_output_str = json.dumps(json_output, indent=2)
        
        toon_data_tokens = count_tokens(toon_input)
        json_data_tokens = count_tokens(json_output_str)
        
        return {
            "output": json_output_str,
            "toon_data_tokens": toon_data_tokens,
            "json_data_tokens": json_data_tokens
        }
    except NotImplementedError:
        raise NotImplementedError(
            "TOON decoder is currently in beta. "
            "Please use a simpler TOON structure or convert JSON to TOON only. "
            "Complex nested objects may not be fully supported yet."
        )
    except Exception as e:
        raise Exception(f"[TOON decode failed] Structure not supported: {str(e)}")

import time

def query_data_with_gemini_util(data_text: str, question: str, data_format: str):
    """Query and analyze data using Gemini AI"""
    start_time = time.time()
    
    if not GEMINI_API_KEY:
        return {"error": "Gemini API key not configured"}
    
    # Set project name based on input format
    project_name = "json-query" if data_format == "JSON" else "toon-query"
    
    # Convert data and count tokens for comparison
    json_text = None
    toon_text = None
    json_data_tokens = 0
    toon_data_tokens = 0
    conversion_status = "success"
    
    try:
        if data_format == "JSON":
            json_text = data_text
            json_data_tokens = count_tokens(json_text)
            # Convert to TOON
            data_obj = json.loads(json_text)
            toon_text = toon_encoder.encode(data_obj, options={"indent": 2, "delimiter": ","})
            toon_data_tokens = count_tokens(toon_text)
        else:  # TOON
            toon_text = data_text
            toon_data_tokens = count_tokens(toon_text)
            # Convert to JSON
            data_obj = toon_encoder.decode(toon_text)
            json_text = json.dumps(data_obj, indent=2)
            json_data_tokens = count_tokens(json_text)
    except Exception as e:
        # Conversion failed
        conversion_status = "failed"
        json_data_tokens = count_tokens(data_text) if data_format == "JSON" else 0
        toon_data_tokens = count_tokens(data_text) if data_format == "TOON" else 0
    
    # Create prompt for Gemini
    prompt = f"""You are a data analysis assistant. Analyze the following {data_format} data and answer the question.

Data:
```
{data_text}
```

Question: {question}

Provide a clear, concise answer. If the question requires calculations, show your work. If the data doesn't contain the information needed, say so."""
    
    # Create traceable function for Gemini query
    @traceable(
        name=f"{data_format.lower()}_query",
        project_name=project_name,
        run_type="llm",
        metadata={
            "model": "gemini-2.5-flash"
        }
    )
    def _gemini_query(prompt_text, input_tokens):
        # Use cached model if available
        model = GEMINI_MODEL
        if not model:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
        response = model.generate_content(prompt_text)
        answer_text = response.text
        output_tokens = count_tokens(answer_text)
        
        return {
            "answer": answer_text,
            "usage": {
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens
            }
        }
    
    # Count component tokens for detailed breakdown
    data_tokens = count_tokens(data_text)
    question_tokens = count_tokens(question)
    prompt_tokens = count_tokens(prompt)
    template_tokens = max(0, prompt_tokens - (data_tokens + question_tokens))
    
    # Execute query
    result = _gemini_query(prompt, prompt_tokens)
    answer = result["answer"]
    completion_tokens = result["usage"]["completion_tokens"]
    total_llm_tokens = result["usage"]["total_tokens"]
    
    # Calculate execution time
    exec_ms = round((time.time() - start_time) * 1000, 2)
    
    # Calculate savings only if conversion succeeded
    data_savings_tokens = 0
    data_savings_percent = 0.0
    
    if conversion_status == "success" and json_data_tokens > 0:
        data_savings_tokens = json_data_tokens - toon_data_tokens
        data_savings_percent = (data_savings_tokens / json_data_tokens) * 100
    
    return {
        "answer": answer,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_llm_tokens": total_llm_tokens,
        "breakdown": {
            "data_tokens": data_tokens,
            "question_tokens": question_tokens,
            "template_tokens": template_tokens
        },
        "data_format": data_format,
        "json_data_tokens": json_data_tokens,
        "toon_data_tokens": toon_data_tokens,
        "data_savings_tokens": data_savings_tokens,
        "data_savings_percent": data_savings_percent,
        "conversion_status": conversion_status,
        "exec_ms": exec_ms
    }
