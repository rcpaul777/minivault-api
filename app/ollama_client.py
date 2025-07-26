import ollama, requests, os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def generate_response(prompt: str, model: str = MODEL_NAME):
    try:
        if not is_ollama_available(model):
            raise ConnectionError(f"Ollama server not running at {OLLAMA_BASE_URL}, Please start it using: `ollama run {model}`")
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        raise RuntimeError(f"Failed to generate response: {str(e)}")

def is_ollama_available(model: str):
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            models = [m["name"] for m in response.json().get("models", [])]
            return any(m.startswith(model) for m in models)  # prefix match
        return False
    except requests.exceptions.RequestException:
        return False