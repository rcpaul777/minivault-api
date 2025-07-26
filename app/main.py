import os, time, psutil, requests, traceback
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
from app.logger import log_interaction_for_generate, log_interaction_for_status, log_interaction_error
from app.ollama_client import generate_response

# Load .env values
load_dotenv()

# Defaults from .env or fallback
MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# FastAPI app
app = FastAPI()
start_time = time.time()

# Pydantic model for request validation
class GenerateRequest(BaseModel):
    prompt: str
    model: str = MODEL_NAME
    source: str = "api"

# GET /status
@app.get("/status")
def status(source: str = Query("api", description="Origin of the request")):
    try:
        status_check_response = {
            "app": {
                "start_time": datetime.fromtimestamp(start_time).isoformat(),
                "uptime": format_uptime(time.time() - start_time),
                "api_url": API_BASE_URL
           },
           "system": {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "per_cpu_percent": psutil.cpu_percent(interval=1, percpu=True),
                "memory_percent": psutil.virtual_memory().percent,
                "available_memory_mb": round(psutil.virtual_memory().available / 1024 / 1024, 2),
                "disk_percent": psutil.disk_usage("/").percent,
                "available_disk_gb": round(psutil.disk_usage("/").free / 1024 / 1024 / 1024, 2),
            },
            "ollama": get_ollama_health(),
        }
        log_interaction_for_status(response=status_check_response, source=source)
        return status_check_response
    except Exception as e:
        log_interaction_error(status_code=500, source=source, error=f"Status - Error: {str(e)}", stack_trace=traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Status - Error: {str(e)}")

# POST /generate
@app.post("/generate")
async def generate(request: GenerateRequest):
    try:
        promt_generate_response = generate_response(request.prompt, request.model)
        log_interaction_for_generate(prompt=request.prompt, response=promt_generate_response, model=request.model, source=request.source)
        return {"response": promt_generate_response}
    except Exception as e:
        log_interaction_error(status_code=500, source=request.source, error=f"Model: {request.model} - Error: {str(e)}", stack_trace=traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Model: {request.model} - Error: {str(e)}")
    
# Utility to format uptime
def format_uptime(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"


# Check if Ollama is reachable and list available models
def get_ollama_health():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        response.raise_for_status()
        models = [m["name"] for m in response.json().get("models", [])]
        return {"status": "reachable", "available_models": models}
    except Exception as e:
        return {"status": "unreachable", "available_models": [], "error": str(e)}