import json
import re
import logging

logger = logging.getLogger(__name__)

def extract_json_block(text: str) -> str | None:
    # safer non-greedy match for first full JSON object
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else None


def try_fix_truncated_json(s: str) -> str:
    """
    Basic repair for cut-off JSON (very common in LLMs)
    """
    s = s.strip()

    # try trimming to last valid closing brace
    last_brace = s.rfind("}")
    if last_brace != -1:
        s = s[:last_brace + 1]

    return s


def parse_json_safe(text: str) -> dict:
    if not text:
        return {"error": "Empty response", "raw": ""}

    try:
        text = text.strip()

        json_str = extract_json_block(text)

        if not json_str:
            return {
                "error": "No JSON found",
                "raw": text
            }

        # try parse normally
        try:
            return json.loads(json_str)

        except json.JSONDecodeError:
            logger.warning("JSON invalid, attempting repair")

            fixed = try_fix_truncated_json(json_str)

            try:
                return json.loads(fixed)
            except json.JSONDecodeError as e:
                logger.error(f"Still invalid JSON: {e}")
                return {
                    "error": "Invalid JSON (unfixable)",
                    "raw": json_str
                }

    except Exception as e:
        logger.exception(f"Unexpected parse error: {e}")
        return {
            "error": "Parsing failed",
            "raw": text
        }