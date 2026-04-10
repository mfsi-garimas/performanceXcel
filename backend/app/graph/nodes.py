from app.services.ocr_service import run_ocr
from app.services.llm_service import run_llm
from app.services.rubric_service import extract_rubric
from app.prompts.rubric import build_prompt
from app.prompts.evaluation import build_prompt as build_prompt_evaluate
from app.config.log_config import logger

def ocr_node(state: dict) -> dict:
    """
    Perform OCR on rubric and submission images.
    """
    try:
        logger.info("Starting OCR node", extra={"state_keys": list(state.keys())})

        # Rubric OCR
        if state.get("rubric_images"):
            text_lines = []
            for img in state["rubric_images"]:
                ocr_output = run_ocr(img)
                text_lines.append(ocr_output["ocr_text"])
                state["rubric_text"] = " ".join(text_lines)
                state["rubric_html"] = ocr_output["table_html"]
                logger.debug("Rubric OCR completed", extra={"rubric_text_preview": state["rubric_text"][:200]})

        # Submission OCR
        if state.get("submission_images"):
            text_lines = []
            for img in state["submission_images"]:
                ocr_output = run_ocr(img)
                text_lines.append(ocr_output["ocr_text"])
                state["submission_text"] = " ".join(text_lines)
                logger.debug("Submission OCR completed", extra={"submission_text_preview": state["submission_text"][:200]})

        logger.info("OCR node completed", extra={"state_keys": list(state.keys())})
        return state

    except Exception as e:
        logger.exception("OCR node failed", extra={"state_keys": list(state.keys())})
        raise


def merge_input_node(state: dict) -> dict:
    """
    Merge OCR output with provided text input if images are not provided.
    """
    try:
        state["rubric_text"] = state.get("rubric_text") or state.get("ocr_rubric")
        state["submission_text"] = state.get("submission_text") or state.get("ocr_submission")
        logger.info("Merge input node completed", extra={
            "rubric_present": "rubric_text" in state,
            "submission_present": "submission_text" in state
        })
        return state
    except Exception as e:
        logger.exception("Merge input node failed", extra={"state_keys": list(state.keys())})
        raise


def grading_node(state: dict) -> dict:
    """
    Run grading LLM on rubric text to generate rubric JSON.
    """
    try:
        rubric = state.get("rubric_text")
        rubric_html = state.get("rubric_html","")
        if not rubric:
            raise ValueError("No rubric text available for grading node")

        prompt = build_prompt(rubric, rubric_html)
        result = run_llm(prompt)
        state["rubric_json"] = result

        logger.info("Grading node completed", extra={
            "rubric_json_preview": str(result)[:500]
        })
        return state

    except Exception as e:
        logger.exception("Grading node failed", extra={"state_keys": list(state.keys())})
        raise


def evaluation_node(state: dict) -> dict:
    """
    Evaluate submission against rubric using LLM.
    """
    try:
        rubric_json = state.get("rubric_json")
        submission_text = state.get("submission_text")

        if not rubric_json or not submission_text:
            raise ValueError("Rubric JSON or submission text missing for evaluation node")

        prompt = build_prompt_evaluate(rubric_json, submission_text)
        result = run_llm(prompt)

        state["llm_output"] = result
        state["final_output"] = result

        logger.info("Evaluation node completed", extra={
            "final_output_preview": str(result)[:500]
        })
        return state

    except Exception as e:
        logger.exception("Evaluation node failed", extra={"state_keys": list(state.keys())})
        raise
