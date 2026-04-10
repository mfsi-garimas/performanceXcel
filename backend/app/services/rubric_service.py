from app.services.ocr_service import run_ocr
from app.services.llm_service import run_llm
from app.prompts.rubric import build_prompt
from app.utils.parser import parse_json_safe
from app.config.log_config import logger

def extract_rubric(file_path: str):
    """
    Extract a structured rubric from a file using OCR and LLM.

    Args:
        file_path: Path to the rubric file (PDF, DOCX, or image).

    Returns:
        Parsed JSON object representing the rubric.
    """
    try:
        logger.info("Starting rubric extraction", extra={"file_path": file_path})

        rubric_data = run_ocr(file_path)
        logger.debug("OCR text tokenized", extra={"file_path": file_path})

        prompt = build_prompt(rubric_data)
        logger.debug("Rubric prompt built", extra={"prompt_preview": str(prompt)[:200]})

        raw_output = run_llm(prompt)
        logger.debug("Raw LLM output received", extra={"output_preview": str(raw_output)[:500]})

        parsed_output = parse_json_safe(raw_output)
        if parsed_output is None:
            logger.warning("LLM returned invalid JSON, returning raw output",
                           extra={"file_path": file_path, "raw_output": str(raw_output)[:500]})
            parsed_output = {"raw_output": raw_output}

        logger.info("Rubric extraction complete", extra={"file_path": file_path})
        return parsed_output

    except Exception as e:
        logger.exception("Rubric extraction failed", extra={"file_path": file_path})
        raise