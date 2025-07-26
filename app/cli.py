import argparse, requests, os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def main():
    parser = argparse.ArgumentParser(description="Send prompt to MiniVault API")
    parser.add_argument("--prompt", help="Prompt to send to /generate")
    parser.add_argument("--model", default=MODEL_NAME, help="Model to use (e.g., llama2, mistral)")
    parser.add_argument("--status", action="store_true", help="Check /status endpoint")
    args = parser.parse_args()

    # Handle status check
    if args.status:
        try:
            response = requests.get(f"{API_BASE_URL}/status", params={"source": "cli"})
            response.raise_for_status()
            print(response.json())
        except requests.exceptions.RequestException as e:
            print("Failed to get status: ", e)
        return
    
    # Require --prompt only if not status check
    if not args.prompt:
        parser.error("The --prompt argument is required unless --status is used.")

    # Handle prompt generation
    payload = {"prompt": args.prompt, "model": args.model, "source": "cli"}
    try:
        response = requests.post(f"{API_BASE_URL}/generate", json=payload)
        response.raise_for_status()  # raises exception for 4xx/5xx
        result = response.json()
        print(result["response"])
    except requests.exceptions.RequestException as e:
        print("Failed to get generate response: ", e)
    except (KeyError, ValueError) as e:
        print("Unexpected response format: ", response.text)

if __name__ == "__main__":
    main()