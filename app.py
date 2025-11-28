import streamlit as st
import json
import toon_format as toon_encoder
import tiktoken
from datetime import datetime
import os
from pathlib import Path
from langsmith import Client, trace
from langsmith.run_helpers import traceable
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

# MUST be called first, before any other Streamlit commands
st.set_page_config(page_title="TOON Data & Token Studio", layout="wide")

# Use GPT-4 encoding for token counting
def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

# LangSmith Configuration
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true").lower() == "true"

# Initialize LangSmith client if API key is available
langsmith_client = None
langsmith_connected = False
if LANGSMITH_API_KEY:
    langsmith_client = Client(api_key=LANGSMITH_API_KEY)
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
    langsmith_connected = True

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_configured = False
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_configured = True

# Conversion functions (not logged to LangSmith)
def convert_json_to_toon(json_input, indent, delimiter):
    """Convert JSON to TOON format with token tracking"""
    data = json.loads(json_input)
    toon_output = toon_encoder.encode(data, options={"indent": indent, "delimiter": delimiter})
    
    json_tokens = count_tokens(json_input)
    toon_tokens = count_tokens(toon_output)
    savings = json_tokens - toon_tokens
    savings_percent = (savings / json_tokens) * 100 if json_tokens > 0 else 0
    
    return {
        "output": toon_output,
        "json_tokens": json_tokens,
        "toon_tokens": toon_tokens,
        "savings": savings,
        "savings_percent": savings_percent
    }

def convert_toon_to_json(toon_input):
    """Convert TOON to JSON format with token tracking"""
    try:
        json_output = toon_encoder.decode(toon_input)
        json_output_str = json.dumps(json_output, indent=2)
        
        toon_tokens = count_tokens(toon_input)
        json_tokens = count_tokens(json_output_str)
        
        return {
            "output": json_output_str,
            "toon_tokens": toon_tokens,
            "json_tokens": json_tokens
        }
    except NotImplementedError:
        raise NotImplementedError(
            "TOON decoder is currently in beta. "
            "Please use a simpler TOON structure or convert JSON to TOON only. "
            "Complex nested objects may not be fully supported yet."
        )
    except Exception as e:
        raise Exception(f"Error decoding TOON: {str(e)}")

def query_data_with_gemini(data_text, question, data_format):
    """Query and analyze data using Gemini AI"""
    if not gemini_configured:
        return {"error": "Gemini API key not configured"}
    
    # Use the specified format directly
    original_format = data_format
    
    # Set project name based on input format
    project_name = "json-query" if original_format == "JSON" else "toon-query"
    
    # Convert data and count tokens for comparison (for display only)
    json_text = None
    toon_text = None
    json_tokens = 0
    toon_tokens = 0
    
    try:
        if original_format == "JSON":
            json_text = data_text
            json_tokens = count_tokens(json_text)
            # Convert to TOON
            data_obj = json.loads(json_text)
            toon_text = toon_encoder.encode(data_obj, options={"indent": 2, "delimiter": ","})
            toon_tokens = count_tokens(toon_text)
        else:  # TOON
            toon_text = data_text
            toon_tokens = count_tokens(toon_text)
            # Convert to JSON
            data_obj = toon_encoder.decode(toon_text)
            json_text = json.dumps(data_obj, indent=2)
            json_tokens = count_tokens(json_text)
    except Exception as e:
        # If conversion fails, just use original
        json_tokens = count_tokens(data_text) if original_format == "JSON" else 0
        toon_tokens = count_tokens(data_text) if original_format == "TOON" else 0
    
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
        name=f"{original_format.lower()}_query",
        project_name=project_name,
        run_type="llm",
        metadata={
            "model": "gemini-2.5-pro"
        }
    )
    def _gemini_query(prompt_text, input_tokens):
        model = genai.GenerativeModel('gemini-2.5-pro')
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
    
    # Count prompt tokens
    prompt_tokens = count_tokens(prompt)
    
    # Execute query
    result = _gemini_query(prompt, prompt_tokens)
    answer = result["answer"]
    response_tokens = result["usage"]["completion_tokens"]
    total_tokens = result["usage"]["total_tokens"]
    
    return {
        "answer": answer,
        "prompt_tokens": prompt_tokens,
        "response_tokens": response_tokens,
        "total_tokens": total_tokens,
        "data_format": data_format,
        "json_tokens": json_tokens,
        "toon_tokens": toon_tokens,
        "savings": json_tokens - toon_tokens,
        "savings_percent": ((json_tokens - toon_tokens) / json_tokens * 100) if json_tokens > 0 else 0
    }



st.title("TOON Data & Token Studio")

st.markdown("""
**Compare TOON vs JSON for Token Efficiency**
""")

# Sidebar: LangSmith Connection Status
st.sidebar.title("Connection Status")

# LangSmith Status
if langsmith_connected:
    st.sidebar.success("LangSmith Connected")
else:
    st.sidebar.warning("LangSmith API key not set")
    st.sidebar.caption("Set LANGSMITH_API_KEY environment variable")

# Gemini Status
st.sidebar.divider()
if gemini_configured:
    st.sidebar.success("Gemini AI Ready")
else:
    st.sidebar.warning("Gemini API key not set")
    st.sidebar.caption("Set GEMINI_API_KEY for Query & Analysis")

tab1, tab2, tab3 = st.tabs(["JSON to TOON", "TOON to JSON", "🤖 Query & Analysis"])

with tab1:
    st.header("JSON to TOON")
    col1, col2 = st.columns(2)
    
    with col1:
        json_input = st.text_area("Input JSON", height=400, value='{\n  "name": "Alice",\n  "age": 30,\n  "items": [\n    {"id": 1, "name": "Apple"},\n    {"id": 2, "name": "Banana"}\n  ]\n}')
        
    with col2:
        st.subheader("Options")
        indent = st.number_input("Indent Size", min_value=1, max_value=8, value=2)
        delimiter = st.selectbox("Delimiter", [",", "\\t", "|"], index=0)
        if delimiter == "\\t": delimiter = "\t"
        
        if st.button("Convert to TOON"):
            try:
                result = convert_json_to_toon(json_input, indent, delimiter)
                
                st.success(f"Conversion Successful! Saved {result['savings_percent']:.1f}% tokens.")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("JSON Tokens", result["json_tokens"])
                m2.metric("TOON Tokens", result["toon_tokens"])
                m3.metric("Savings", f"{result['savings']} ({result['savings_percent']:.1f}%)")
                
                st.code(result["output"], language="yaml") # YAML highlighting looks similar enough
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.header("TOON to JSON")
    col1, col2 = st.columns(2)
    
    with col1:
        toon_input = st.text_area("Input TOON", height=400, value='[2,]{id,name}:\n  1,Apple\n  2,Banana')
        
    with col2:
        if st.button("Convert to JSON"):
            try:
                result = convert_toon_to_json(toon_input)
                
                
                st.success(f"Conversion Successful!")
                
                m1, m2 = st.columns(2)
                m1.metric("TOON Tokens", result["toon_tokens"])
                m2.metric("JSON Tokens", result["json_tokens"])
                
                st.code(result["output"], language="json")
            except Exception as e:
                st.error(f"Error: {e}")

with tab3:
    st.header("🤖 Query & Analysis with Gemini")
    
    if not gemini_configured:
        st.warning("⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in your .env file.")
        st.info("Get your API key from: https://makersuite.google.com/app/apikey")
    else:
        st.markdown("Ask questions about your JSON or TOON data using AI.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Data")
            data_input = st.text_area(
                "Paste your JSON or TOON data",
                height=300,
                value='[{"id": 1, "name": "Alice", "age": 30}, {"id": 2, "name": "Bob", "age": 25}]',
                help="Paste JSON or TOON formatted data"
            )
            
            data_format = st.radio(
                "Data Format",
                ["JSON", "TOON"],
                horizontal=True
            )
        
        with col2:
            st.subheader("Question")
            question = st.text_input(
                "What would you like to know?",
                placeholder="e.g., What's the average age?"
            )
            
            # Example questions
            st.caption("Example questions:")
            example_questions = [
                "What's the average age?",
                "List all names",
                "How many items?",
                "Summarize data"
            ]
            
            cols = st.columns(len(example_questions))
            for i, eq in enumerate(example_questions):
                if cols[i].button(eq, key=f"ex_{i}", use_container_width=True):
                    question = eq
            
            st.divider()
            
            if st.button("🔍 Analyze", type="primary", use_container_width=True):
                if not question:
                    st.error("Please enter a question")
                elif not data_input:
                    st.error("Please provide data to analyze")
                else:
                    with st.spinner("Analyzing with Gemini..."):
                        try:
                            result = query_data_with_gemini(data_input, question, data_format)
                            
                            if "error" in result:
                                st.error(result["error"])
                            else:
                                st.success("Analysis complete!")
                                
                                # Show answer
                                st.markdown("### Answer")
                                st.markdown(result["answer"])
                                
                                # Show token usage
                                st.divider()
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Input Tokens", result["prompt_tokens"])
                                col2.metric("Output Tokens", result["response_tokens"])
                                col3.metric("Total Tokens", result["total_tokens"])
                                
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
