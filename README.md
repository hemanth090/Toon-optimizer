# TOON Studio - Token Efficiency Toolkit

**Modern Web Application for JSON/TOON Conversion and AI-Powered Data Analysis**

A full-stack React + Python FastAPI application that converts between JSON and TOON formats, queries data with Google Gemini AI, and provides detailed token efficiency analytics with a sleek, Notion-inspired UI.

---

## ✨ Features

- 🔄 **Bidirectional Conversion**: Seamlessly convert between JSON ↔ TOON formats
- 🤖 **AI-Powered Analysis**: Query your data using Google Gemini 2.5 Flash
- 📊 **Token Tracking**: Real-time token counting and efficiency comparison
- 💰 **Cost Calculator**: Frontend-based pricing display with transparent formula
- 🎨 **Notion-Inspired UI**: Slim, sleek design with warm color palette
- 📋 **Copy Feedback**: "Copied successfully" confirmation messages
- 📈 **LangSmith Integration**: Complete observability for AI queries (optional)

---

## 🏗️ Architecture

### Backend (Python FastAPI)
- RESTful API for conversions and AI queries
- Google Gemini 2.5 Flash integration
- LangSmith tracing for observability
- Token counting with official model tokenizers
- CORS-enabled for production deployment

### Frontend (React + Vite)
- Modern component-based architecture
- Real-time API communication
- Frontend cost calculation (Gemini 2.5 Flash pricing)
- Responsive, Notion-inspired design
- Environment-based API URL configuration

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**
- **Google Gemini API key** (required)
- **LangSmith API key** (optional)

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
   
   Copy the example file:
   ```bash
   copy .env.example .env  # Windows
   # cp .env.example .env  # macOS/Linux
   ```
   
   Edit `.env` and add your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   LANGSMITH_API_KEY=your_langsmith_api_key_here  # Optional
   LANGSMITH_TRACING=true  # Optional
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

3. **Configure environment variables (optional for local dev)**
   
   The frontend uses `http://localhost:8000` by default. For production, create `.env.production`:
   ```env
   VITE_API_BASE_URL=https://your-backend-url.onrender.com
   ```

---

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Available at:**
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

**Available at:** `http://localhost:5173`

---

## 🔑 Getting API Keys

### Google Gemini API Key (Required)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key to your `backend/.env` file

### LangSmith API Key (Optional - for observability)

1. Visit [LangSmith Settings](https://smith.langchain.com/settings)
2. Sign in or create a free account
3. Navigate to **"API Keys"**
4. Create a new API key
5. Copy to your `backend/.env` file

---

## 📖 Features Guide

### JSON to TOON Conversion
1. Navigate to the **"JSON to TOON"** tab
2. Paste your JSON data
3. Configure indent size and delimiter (comma, tab, or pipe)
4. Click **"🚀 Convert to TOON"**
5. View token savings percentage
6. Click **"📋 Copy to Clipboard"** (shows "✓ Copied successfully")

### TOON to JSON Conversion
1. Navigate to the **"TOON to JSON"** tab
2. Paste your TOON formatted data
3. Click **"🚀 Convert to JSON"**
4. View token comparison metrics
5. Copy the JSON output

### Query & Analysis (AI-Powered)
1. Navigate to the **"Query & Analysis"** tab
2. Select format: **JSON** or **TOON**
3. Paste your data
4. Enter a question or click an example
5. Click **"🔍 Analyze"**
6. View AI-generated answer
7. See detailed token usage and cost breakdown

**Cost Transparency:**
- Shows exact pricing: `$0.15 per million tokens in • $0.60 per million tokens out`
- Displays calculated cost with 6 decimal precision
- Uses official Gemini 2.5 Flash pricing

---

## 📂 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── utils.py             # Conversion & AI utility functions
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile             # Render deployment config
│   └── .env.example         # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── JsonToToon.jsx
│   │   │   ├── ToonToJson.jsx
│   │   │   ├── QueryAnalysis.jsx
│   │   │   └── StatusIndicator.jsx
│   │   ├── services/        # API service layer
│   │   │   └── api.js
│   │   ├── App.jsx          # Main app component
│   │   ├── App.css          # Global Notion-inspired styles
│   │   └── index.css        # Design system variables
│   ├── package.json         # Node dependencies
│   ├── vercel.json          # Vercel deployment config
│   └── .env.production.example  # Production env template
├── .gitignore               # Git exclusions (protects .env)
└── README.md                # This file
```

---

## 🛠️ API Endpoints

### Conversion Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/convert/json-to-toon` | Convert JSON to TOON format |
| `POST` | `/api/convert/toon-to-json` | Convert TOON to JSON format |

### Query Endpoint
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/query` | Query data with Gemini AI |
| `POST` | `/api/count` | Count tokens in text |

### Status Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check (API status) |
| `GET` | `/api/status` | API key configuration status |

---

## 🎨 What is TOON?

TOON is a **compact, human-readable serialization format** optimized for LLM contexts. It significantly reduces token usage compared to JSON while maintaining excellent readability.

**Token Savings Example:**

```json
// JSON Format (102 tokens)
[
  {"id": 1, "name": "Alice", "age": 30},
  {"id": 2, "name": "Bob", "age": 25}
]

// TOON Format (36 tokens) - 65% savings!
[2,]{id,name,age}:
  1,Alice,30
  2,Bob,25
```

**Benefits:**
- � **30-70% token reduction** for structured data
- 💰 **Lower API costs** for LLM operations
- 👁️ **Human-readable** format
- ⚡ **Faster processing** due to fewer tokens

---

## 🎨 Design System

The UI follows a **Notion-inspired design philosophy**:

- **Colors**: Warm neutrals (#F7F6F3, #37352F)
- **Typography**: Inter font family
- **Spacing**: Slim, compact scale (14/22/28px)
- **Buttons**: Dark gray instead of blue
- **Shadows**: Subtle, professional elevation
- **Interactions**: Smooth cubic-bezier transitions

---

## 🔒 Security Notes

- ✅ `.env` files are excluded from Git via `.gitignore`
- ✅ Never commit API keys to version control
- ✅ Use `.env.example` as templates only
- ✅ CORS is configurable for production domains
- ✅ Environment variables are validated on startup

---

## 🚢 Deployment

### Deploy Backend on Render

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: Uses `Procfile` automatically
5. Add environment variables:
   ```
   GEMINI_API_KEY=<your-key>
   LANGSMITH_API_KEY=<your-key>  # Optional
   ```
6. Deploy and copy your backend URL

### Deploy Frontend on Vercel

1. Import your GitHub repository on [Vercel](https://vercel.com)
2. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add environment variable:
   ```
   VITE_API_BASE_URL=https://your-backend.onrender.com
   ```
4. Deploy!

**Your app will be live at:**
- Frontend: `https://your-project.vercel.app`
- Backend: `https://your-backend.onrender.com`

---

## 💡 Usage Tips

1. **First Time Setup**: 
   - Get your Gemini API key first (required)
   - LangSmith is optional but recommended for production

2. **Development**:
   - Backend auto-reloads on code changes (`--reload`)
   - Frontend has fast HMR with Vite
   - Check `/docs` for interactive API documentation

3. **Production**:
   - Update CORS in `backend/main.py` with your Vercel domain
   - Use `.env.production` for frontend API URL
   - Monitor costs with the built-in pricing calculator

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Hemanth Naveen**  
GitHub: [@hemanth090](https://github.com/hemanth090)  
Email: naveenhemanth4@gmail.com

---

## 🙏 Acknowledgments

- [TOON Format](https://github.com/google/toon) - Compact serialization for LLMs
- [Google Gemini](https://ai.google.dev/) - Powerful AI model for data analysis
- [LangSmith](https://smith.langchain.com/) - LLM observability platform
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - JavaScript UI library
- [Vite](https://vitejs.dev/) - Next generation frontend tooling
- [Notion](https://notion.so/) - Design inspiration

---

## 📄 License

**MIT License** - Feel free to use this project for your own purposes!

---

## 📊 Stats

- **Token Savings**: Up to 70% reduction with TOON
- **Gemini Pricing**: $0.15/1M input + $0.60/1M output
- **Deployment**: Free tier available on Vercel + Render
- **Response Time**: <1s for typical queries

---

**⭐ Star this repo if you find it useful!**
