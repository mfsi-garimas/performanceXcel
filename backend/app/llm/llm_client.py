import requests
from app.config.log_config import logger
from app.config.env_config import settings

OLLAMA_URL = settings.OLLAMA_URL
MODEL_NAME = settings.MODEL_NAME

session = requests.Session()

def generate(prompt: str):
    try:
        logger.info("Sending request to Ollama API", extra={
            "model": MODEL_NAME,
            "prompt_preview": prompt[:200]
        })

        response = session.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 300,     
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_ctx": 2048      
                }
            },
            timeout=180  
        )

        response.raise_for_status()
        data = response.json()

        if "response" not in data:
            logger.error("Invalid Ollama response", extra={"data": data})
            raise ValueError("Invalid Ollama response format")

        return data["response"]

    except requests.exceptions.RequestException:
        logger.exception("Ollama API request failed")
        raise