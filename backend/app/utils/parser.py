import json
import re
import logging

logger = logging.getLogger(__name__)

def parse_json_safe(text: str) -> dict:
    if not text:
        return {"error": "Empty response", "raw": ""}

    try:
        text = text.strip()

        # Extract JSON block
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            json_str = match.group(0)

            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                return {
                    "error": "Invalid JSON",
                    "raw": json_str
                }

        return {
            "error": "No JSON found",
            "raw": text
        }

    except Exception as e:
        logger.error(f"Unexpected parse error: {e}")
        return {
            "error": "Parsing failed",
            "raw": text
        }