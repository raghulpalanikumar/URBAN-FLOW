import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAMES = ["phi:latest", "phi", "llama3.2:latest", "llama3.2", "tinyllama:latest", "tinyllama"]
OLLAMA_TIMEOUT = 120

def _try_model(prompt, model_name):
    """Try a single model. Returns (success, response_text_or_error)."""
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3},
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=OLLAMA_TIMEOUT)
        if response.status_code == 200:
            return True, response.json().get("response", "")
        # Capture 500 body for debugging
        try:
            body = response.json()
            detail = body.get("error", response.text[:200])
        except Exception:
            detail = response.text[:200] if response.text else response.reason
        return False, f"Ollama returned {response.status_code}: {detail}"
    except requests.exceptions.ConnectionError:
        return False, "Ollama is not reachable. Please start Ollama (e.g. install from https://ollama.ai and run: ollama pull phi)."
    except requests.exceptions.Timeout:
        return False, "Ollama request timed out. Try a smaller model (e.g. ollama pull tinyllama)."
    except requests.exceptions.RequestException as e:
        return False, str(e)

def query_ollama(prompt):
    for model in MODEL_NAMES:
        print(f"Sending prompt to Ollama (model={model})...")
        ok, result = _try_model(prompt, model)
        if ok:
            print("Ollama response received.")
            return result
        print(f"Ollama failed with {model}: {result}")
    # All models failed; return a single error message (no "Error:" prefix so caller can treat as generic failure)
    return "Error: Reasoning engine unavailable. Start Ollama and run: ollama pull phi"

def get_model_name():
    return MODEL_NAMES[0]
