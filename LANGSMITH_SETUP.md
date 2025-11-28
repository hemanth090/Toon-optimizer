# LangSmith Setup Instructions

## Step 1: Get Your LangSmith API Key

1. Go to [https://smith.langchain.com/settings](https://smith.langchain.com/settings)
2. Sign in or create an account
3. Navigate to "API Keys" section
4. Create a new API key or copy an existing one

## Step 2: Set Environment Variable

### Windows (PowerShell):
```powershell
$env:LANGSMITH_API_KEY="your_api_key_here"
```

### Windows (Command Prompt):
```cmd
set LANGSMITH_API_KEY=your_api_key_here
```

### Linux/Mac:
```bash
export LANGSMITH_API_KEY="your_api_key_here"
```

### Or create a `.env` file:
Create a file named `.env` in the project directory:
```
LANGSMITH_API_KEY=your_api_key_here
LANGSMITH_TRACING=true
```

Then install python-dotenv and load it:
```bash
pip install python-dotenv
```

Add to the top of `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Step 3: Restart Streamlit

After setting the environment variable, restart your Streamlit app:
```bash
streamlit run app.py
```

## Step 4: Verify Connection

- The sidebar should show "✅ LangSmith Connected"
- Perform a conversion
- Check your LangSmith dashboard at [https://smith.langchain.com](https://smith.langchain.com)
- You should see traces under projects:
  - `json-to-toon` for JSON → TOON conversions
  - `toon-to-json` for TOON → JSON conversions

## Troubleshooting

If you see "⚠️ LangSmith API key not set":
1. Make sure you set the environment variable correctly
2. Restart the terminal/PowerShell window
3. Restart the Streamlit app
4. Check that the API key is valid
