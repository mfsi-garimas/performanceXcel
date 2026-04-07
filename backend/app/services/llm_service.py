import json
from app.utils.parser import parse_json_safe
from app.llm.llm_client import generate
from app.config.log_config import logger

def run_llm(prompt):
    try:
        logger.info("Sending prompt to LLM", extra={"prompt": prompt[:200]})  
        response = generate(prompt)
        logger.debug("Raw LLM response received", extra={"response": response[:500]}) 

        result = parse_json_safe(response)

        if result is None:
            logger.warning("LLM returned invalid JSON, returning raw text", extra={"response": response[:500]})
            result = {"raw_text": response}

        return result

    except Exception as e:
        logger.exception("LLM processing failed", extra={"prompt": prompt[:200]})
        raise