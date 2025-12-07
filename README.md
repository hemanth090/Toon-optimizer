# TOON Studio - Token Efficiency Toolkit

**A pragmatic tool to benchmark and optimize LLM token costs.**

TOON Studio is a full-stack application designed to explore the **[TOON](https://pypi.org/project/toon-format/) (Token-Oriented Object Notation)** format. It provides real-time conversion, token counting, and AI-powered analysis to help developers understand where and how to save on LLM API costs.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![React](https://img.shields.io/badge/react-18-blue)
![Tests](https://img.shields.io/badge/tests-10%20passing-green)

---

## 🎯 What Problem Does This Solve?

Sending JSON to LLMs wastes tokens on syntax (`{`, `}`, `"`, `:`).
**TOON** format removes this overhead by using a header-defined structure, similar to a CSV but for objects.

**Measured Results with this Tool:**
- **Simple Objects**: ~33% token reduction
- **Large Arrays**: ~52% token reduction (Verified with Gemini tokenizer)

---

## ✨ Features

- **🔄 Bidirectional Conversion**: Convert JSON ↔ TOON instantly.
- **📊 Real-Time Analytics**: See exact token counts and cost savings as you type.
- **🤖 AI Integration**: Query your data using **Google Gemini 2.5 Flash**.
- **💰 Cost Calculator**: Live pricing estimate based on specific model rates.
- **🔎 Observability**: Integrated **LangSmith** tracing for query debugging.
- **✅ Production Ready**: CORS security, proper error handling, and unit tests.

---

## 🏗️ Tech Stack

### Backend
- **Python FastAPI**: High-performance API framework
- **Google Gemini SDK**: Logic and reasoning engine
- **Tiktoken**: Fallback token counting
- **Pytest**: Comprehensive test suite (10 passing tests)

### Frontend
- **React + Vite**: Fast, modern UI
- **CSS Modules**: Clean, component-scoped styling
- **Notion-Inspired Design**: Minimalist and focus-driven

---

## � Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Gemini API Key

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GEMINI_API_KEY in .env
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Run Tests
We believe in reliability. This project includes a test suite verifying conversions and token counting.
```bash
cd backend
pytest test_utils.py -v
```

---

## 🧪 How It Works (The Technical Bit)

TOON optimizes by declaring keys once.

**JSON (37 tokens):**
```json
[{"id": 1, "name": "Alice", "age": 30}, {"id": 2, "name": "Bob", "age": 25}]
```

**TOON (24 tokens):**
```text
[2]{id,name,age}:
  1,Alice,30
  2,Bob,25
```

The header `[2]{id,name,age}` tells the LLM to expect 2 items with those specific keys. The data follows in a clean, comma-separated format.

---

## ⚠️ Known Limitations

- **Decoder Beta**: The TOON decoder is currently in beta. Complex nested structures may not convert back to JSON perfectly.
- **Input Optimization**: TOON is best used for **input** (prompt) optimization. LLMs will typically still generate JSON outputs.

---

## 🤝 Contributing

Contributions are welcome! Please run the test suite before submitting a PR.

**GitHub**: [@hemanth090](https://github.com/hemanth090)

---

*This project is for educational and benchmarking purposes. Always validate data formats before using in production critical paths.*
