# 📦 "MiniVault API": ModelVault Take-Home Project

## 🧠 Overview

This project is a lightweight, local-first REST API to simulate a core ModelVault feature: sending prompts to a local LLM (like `llama2` via Ollama), and returning offline responses.

## ✅ Features

- `POST /generate`: Accepts a prompt and returns an LLM-generated response
- `GET /status`: Shows system stats like CPU, memory, uptime
- Request/response JSONL logging to `logs/log.jsonl`
- CLI for interacting with the API
- Docker + Compose support
- Queueing and concurrency control
- `.env` support for model selection
- Basic tests with `pytest`

----

## 📁 Project Structure

minivault-api/
├── app/
│   ├── __init__.py           # Python module recognition
|   ├── cli.py                # CLI entry point for testing /generate and model override
│   ├── logger.py             # JSONL logger for prompts/responses (with size limit)
|   ├── main.py               # FastAPI app with /generate and /status
│   └── ollama_client.py      # Handles local LLM interaction via Ollama
├── logs/
│   └── log.jsonl             # Persisted request/response logs (rotated)
├── tests/
|   ├── __init__.py           # Python module recognition
│   └── test_main.py           # Basic pytest tests
├── .dockerignore             # Docker ignore file
├── .env                      # Environment variables
├── .gitignore                # Git ignore file
├── docker-compose.yml        # Docker Compose for containerized setup
├── Dockerfile                # Docker build file
├── package-lock.json         # Package lock file
├── package.json              # Package file
├── README.md                 # Setup, usage, and design notes
└── requirements.txt          # Python dependencies

----

## 🚀 Quick Start

### Prerequisites
- [Python 3.11+](https://www.python.org/downloads/)
- [Ollama](https://ollama.com/) with a model like `llama2`
- [Docker](https://www.docker.com/products/docker-desktop) (optional)

----

## 🛠️ Setup Instructions
```bash
# Clone Repository
git clone https://github.com/rcpaul777/minivault-api.git
cd minivault-api

# Create Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv/Scripts/activate
```

### 1. Run Locally
```bash
# Install Dependencies
pip install -r requirements.txt

# Start Ollama Model in Background
ollama run llama2         # or mistral # or both

# Launch FastAPI Server
uvicorn app.main:app --reload

# Try in another bash terminal CLI using curl or try in Postman
curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"prompt": "Hello, who are you?"}'
curl "http://localhost:8000/status"
```

### 2. Using the CLI
```bash
# Try in another bash terminal CLI
python app/cli.py --prompt "Hello, who are you?"  # Default ollama model llama2 is set in .env file
python app/cli.py --prompt "Hello" --model mistral
python app/cli.py --prompt "Hello" --model llama2 --base_url http://192.168.1.100:8080
python app/cli.py --status
```

### 3. With Docker
```bash
# Start Ollama Model in Background
ollama run llama2

# Build and run
docker-compose up --build
```

The API will be available at: `http://localhost:8000`

----

## ✅ API Endpoints:

### 1. `POST /generate`
**Input**
```json
{ "prompt": "Hello, who are you?" }
```
**Response**
```json
{ "response": "I'm a local AI model, running offline!" }
```

### 2. `GET /status`
**Response:**
```json
{
  "app": {
    "start_time": "2025-07-26T13:00:01.123456",
    "uptime": "00:20:14",
    "api_url": "http://localhost:8000"
  },
  "system": {
    "cpu_percent": 12.5,
    "per_cpu_percent": [10.0, 13.0, 12.0, 15.0],
    "memory_percent": 48.2,
    "available_memory_mb": 8192.0,
    "disk_percent": 61.4,
    "available_disk_gb": 120.57
  },
  "ollama": {
    "status": "reachable",
    "available_models": [
      "llama2:latest"
    ]
  }
}
```

----

## 🧾 Logging

All requests and responses are logged to `logs/log.jsonl` in JSON Lines format:

```json
{"timestamp": "2025-07-26T20:46:32.809437+00:00", "source": "test", "model": "llama2", "prompt": "What's your name?", "response": "I'm just an AI, I don't have a personal name. My purpose is to assist and provide helpful responses to the best of my ability. How may I help you today?"}
```

----

## 🏆 Design Highlights
- Local-first: No external APIs or cloud LLMs
- Ollama integration for real local model
- JSONL logs with rotation
- Lightweight Docker setup
- CLI + `.env` model override
- Async prompt queue
- Pytest-based test coverage

---

## 🤔 Improvements / Tradeoffs
- Model concurrency is basic — more advanced queue control could improve speed
- Future: Add SQLite or local caching for duplicate prompt efficiency
- Could support multiple models in memory with warm pool

---

## 🙏 Thanks!
This project was a blast! Built with ❤️ as a take-home for ModelVault.