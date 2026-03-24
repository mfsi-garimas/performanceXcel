import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate(prompt: str):
    response = requests.post(OLLAMA_URL, json={
        "model": "gemma3:4b",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]