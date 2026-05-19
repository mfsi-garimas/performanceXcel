import json

from app.config.env_config import settings
from app.config.log_config import logger

from app.services.ocr_service import run_ocr
from app.services.llm_ocr_service import ocr_with_llm


def extract_ocr(
    image_paths,
    prompt: str = None,
    output_format:str="json"
):
    """
    Unified OCR interface.

    Supports:
    - PaddleOCR
    - LLM OCR (Bedrock)
    """

    provider = settings.OCR_PROVIDER.upper()

    logger.info(
        "OCR provider selected",
        extra={"provider": provider}
    )

    if provider == "LLM":

        ocr_output= ocr_with_llm(
            image_paths=image_paths,
            prompt=prompt,
            output_format=output_format
        )

        if(output_format == 'json'):
            if isinstance(ocr_output, str):
                try:
                    ocr_output = json.loads(ocr_output)
                except json.JSONDecodeError:
                    logger.error(
                        "OCR output is not valid JSON",
                        extra={"ocr_output": ocr_output}
                    )
        
            if not isinstance(ocr_output, (dict, list)):
                logger.error(
                    "OCR output is not JSON object/list",
                    extra={"ocr_output_type": str(type(ocr_output))}
                )

        return {
            "ocr_text": "",
            "table_html": "",
            "llm_output": ocr_output
        }

    elif provider == "PADDLEOCR":
        all_text = []
        all_html = []

        for image_path in image_paths:

            result = run_ocr(image_path)

            ocr_text = result.get("ocr_text", "").strip()
            table_html = result.get("table_html", "").strip()

            if ocr_text:
                all_text.append(ocr_text)

            if table_html:
                all_html.append(table_html)

        return {
            "ocr_text": "\n".join(all_text) if all_text else None,
            "table_html": "\n".join(all_html) if all_html else None,
            "llm_output": None
        }

    else:
        raise ValueError(
            f"Unsupported OCR provider: {provider}"
        )