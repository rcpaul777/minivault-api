import os, pytest, requests
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from app.main import app

load_dotenv()

client = TestClient(app)

MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def get_available_models():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [m["name"].split(":")[0] for m in models]  # get base model name without tag
        return []
    except requests.RequestException:
        return []

available_models = get_available_models()

@pytest.mark.parametrize("model", available_models or ["__skip__"])
def test_generate(model):
    if model == "__skip__":
        pytest.skip("No available models found from Ollama to test.")
    payload = {"prompt": "What's your name?", "model": model, "source": "test"}
    response = requests.post(f"{API_BASE_URL}/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)

def test_invalid_model():
    payload = {"prompt": "Hello", "model": "nonexistent-model", "source": "test"}
    response = requests.post(f"{API_BASE_URL}/generate", json=payload)
    assert response.status_code in (400, 422, 500)

def test_status():
    response = client.get("/status", params={"source": "test"})
    assert response.status_code == 200
    json_data = response.json()
    assert "app" in json_data
    assert "system" in json_data
    assert "ollama" in json_data