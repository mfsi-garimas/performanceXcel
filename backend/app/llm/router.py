from app.llm.llm_client import generate_ollama
from app.llm.bedrock_client import bedrock_service
from app.config.env_config import settings

LLM_USED = settings.LLM_USED

def generate(prompt):

    if(LLM_USED == "BEDROCK"):
        return bedrock_service.generate(prompt)
    elif(LLM_USED == "OLLAMA"):
        return generate_ollama(prompt)
    else:
        raise ValueError(f"Unsupported LLM: {LLM_USED}")