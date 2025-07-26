import os, json
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

LOG_PATH = os.getenv("LOG_PATH", os.path.join("logs", "log.jsonl"))
MAX_LOG_SIZE_MB = int(os.getenv("MAX_LOG_SIZE_MB", 5))  # default = 5 MB

def log_interaction_for_generate(prompt: str, response: str, model: str, source: str):
    """
    Logs prompt-generated-response interaction to a JSONL file.
    Args:
        prompt (str): User input
        response (str): Model-generated response
        model (str): Model used (e.g., llama2, mistral)
        source (str): Origin of the request - 'api' or 'cli' or 'test'
    """
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    rotate_log_if_needed()
    log_data = {
        "timestamp":datetime.now(timezone.utc).isoformat(),
        "source": source,
        "model": model,
        "prompt": prompt,
        "response": response
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data) + "\n")

def log_interaction_for_status(response: str, source: str):
    """
    Logs status-check-response interaction to a JSONL file.
    Args:
        response (str): Status-check response
        source (str): Origin of the request - 'api' or 'cli' or 'test'
    """
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    rotate_log_if_needed()
    log_data = {
        "timestamp":datetime.now(timezone.utc).isoformat(),
        "source": source,
        "prompt": "Status",
        "response": response
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data) + "\n")

def log_interaction_error(status_code: int, source: str, error: str, stack_trace: str):
    """
    Logs an error interaction to the log file.
    Args:
        status_code (int): HTTP status code
        source (str): Origin of the request - 'api' or 'cli' or 'test'
        error (str): Error message
        stack_trace (str): Stack trace of the error
    """
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    rotate_log_if_needed()
    log_data = {
        "timestamp":datetime.now(timezone.utc).isoformat(),
        "source": source,
        "prompt": "Error",
        "error": "Status Code: " + str(status_code) + " - " + error,
        "stack_trace": stack_trace
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data) + "\n")

def rotate_log_if_needed():
    if os.path.exists(LOG_PATH) and os.path.getsize(LOG_PATH) > MAX_LOG_SIZE_MB * 1024 * 1024:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        rotated_path = f"{LOG_PATH.rsplit('.', 1)[0]}_{timestamp}.jsonl"
        os.rename(LOG_PATH, rotated_path)