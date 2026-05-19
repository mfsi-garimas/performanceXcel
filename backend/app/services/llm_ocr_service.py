import json

from app.config.log_config import logger
from app.llm.bedrock_client import bedrock_service
from app.prompts.rubric import (
    build_prompt_ocr_with_JSON_formatting
)


def ocr_with_llm(image_paths, prompt: str, output_format:str ="json") -> dict:
    """
    Single call:
    1. OCR extraction
    2. Table understanding
    3. Rubric structuring
    4. Final JSON generation
    """

    try:
        response_text = bedrock_service.generate(
            prompt=prompt,
            image_paths=image_paths
        )

        logger.info(
            "LLM response",
            extra={"llm_response": response_text}
        )

        logger.info(
            "Output Format",
            extra={"output_format": output_format}
        )

        if(output_format == "json"):
            cleaned_response = (
                response_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(cleaned_response)

        else:
            return response_text

    except Exception as e:
        logger.exception(
            "Extraction failed",
            extra={
                "error": str(e)
            }
        )

        return {}