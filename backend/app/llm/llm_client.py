import requests
from app.config.log_config import logger

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"

def generate(prompt: str):
    """
    Call Ollama API to generate text from a prompt.

    Args:
        prompt: The text prompt to send.

    Returns:
        The response string from the model.

    Raises:
        Exception if the API call fails or response is invalid.
    """
    try:
        logger.info("Sending request to Ollama API", extra={"model": MODEL_NAME, "prompt_preview": prompt[:200]})
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }) 

        logger.debug("Ollama raw response", extra={"status_code": response.status_code, "text": response.text[:500]})

        response.raise_for_status() 
        data = response.json()
        if "response" not in data:
            logger.error("Ollama response missing 'response' key", extra={"data": data})
            raise ValueError("Invalid Ollama response format")

        return data["response"]

    except requests.exceptions.RequestException as e:
        logger.exception("Ollama API request failed", extra={"prompt_preview": prompt[:200]})
        raise
    except Exception as e:
        logger.exception("Failed to process Ollama response", extra={"prompt_preview": prompt[:200]})
        raise