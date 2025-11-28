# TOON Data & Token Studio

**Modern Web Application for JSON/TOON Conversion and AI Analysis**

A React + Python FastAPI application for converting between JSON and TOON formats, querying data with Google Gemini AI, and monitoring token efficiency.

## ✨ Features

- 🔄 **Bidirectional Conversion**: JSON ↔ TOON format conversion
- 🤖 **AI-Powered Analysis**: Query your data using Google Gemini
- 📊 **Token Tracking**: Compare token efficiency between formats
- 🎨 **Modern UI**: Beautiful dark theme with glassmorphism effects
- 📈 **LangSmith Integration**: Full observability for AI queries

## 🏗️ Architecture

### Backend (Python FastAPI)
- RESTful API for conversions and queries
- LangSmith tracing integration
- Token counting with tiktoken
- CORS support for React frontend

### Frontend (React + Vite)
- Modern component-based UI
- Real-time API communication
- Premium dark theme design
- Responsive layout

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   copy .env.example .env  # Windows
   # cp .env.example .env  # macOS/Linux
   ```
   
   Edit `.env` and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   LANGSMITH_API_KEY=your_langsmith_api_key_here  # Optional
   LANGSMITH_TRACING=true
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   copy .env.example .env  # Windows
   # cp .env.example .env  # macOS/Linux
   ```

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The app will open at `http://localhost:5173`

## 🔑 Getting API Keys

### Google Gemini API Key (Required)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy to backend `.env` file

### LangSmith API Key (Optional)
1. Visit [LangSmith Settings](https://smith.langchain.com/settings)
2. Sign in or create an account
3. Navigate to "API Keys"
4. Create a new API key
5. Copy to backend `.env` file

## 📖 Features Guide

### JSON to TOON Conversion
1. Navigate to "JSON to TOON" tab
2. Paste your JSON data
3. Configure indent size and delimiter
4. Click "Convert to TOON"
5. View token savings and copy result

### TOON to JSON Conversion
1. Navigate to "TOON to JSON" tab
2. Paste your TOON data
3. Click "Convert to JSON"
4. View result and token comparison

### Query & Analysis
1. Navigate to "Query & Analysis" tab
2. Paste JSON or TOON data
3. Select data format
4. Enter your question or use examples
5. Click "Analyze" to get AI-powered answers
6. View token usage metrics

## 📂 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── utils.py             # Utility functions
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API service layer
│   │   ├── App.jsx          # Main app component
│   │   └── App.css          # Global styles
│   ├── package.json         # Node dependencies
│   └── .env.example         # Environment template
└── README.md                # This file
```

## 🛠️ API Endpoints

### Conversion Endpoints
- `POST /api/convert/json-to-toon` - Convert JSON to TOON
- `POST /api/convert/toon-to-json` - Convert TOON to JSON

### Query Endpoint
- `POST /api/query` - Query data with Gemini AI

### Status Endpoints
- `GET /api/health` - Health check
- `GET /api/status` - API key configuration status

## 🎨 What is TOON?

TOON is a compact, human-readable serialization format optimized for LLM contexts. It significantly reduces token usage compared to JSON while maintaining readability.

**Example:**
```json
// JSON (more tokens)
[{"id": 1, "name": "Apple"}, {"id": 2, "name": "Banana"}]

// TOON (fewer tokens)
[2,]{id,name}:
  1,Apple
  2,Banana
```

## 🔒 Security Notes

- Never commit `.env` files to Git
- Keep your API keys secure
- Use `.env.example` as templates only
- The `.gitignore` file prevents accidental commits

## 🚢 Deployment

### Backend Deployment
- Deploy to platforms like Railway, Render, or AWS
- Set environment variables in platform settings
- Update CORS origins in `main.py` for production URL

### Frontend Deployment
- Build: `npm run build`
- Deploy `dist/` folder to Vercel, Netlify, or similar
- Update `VITE_API_BASE_URL` to production backend URL

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👨‍💻 Author

[Hemanth](https://github.com/hemanth090)

## 🙏 Acknowledgments

- [TOON Format](https://github.com/toon-format/toon-format) - Compact serialization format
- [LangSmith](https://smith.langchain.com/) - LLM observability platform
- [Google Gemini](https://ai.google.dev/) - AI model for data analysis
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - JavaScript UI library
- [Vite](https://vitejs.dev/) - Next generation frontend tooling

## 📄 License

MIT License - feel free to use this project for your own purposes!
