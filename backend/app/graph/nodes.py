from app.services.llm_ocr_service import ocr_with_llm
from app.services.ocr_service import run_ocr
from app.services.ocr_provider import extract_ocr

from app.services.llm_service import run_llm
from app.services.rubric_service import extract_rubric
from app.prompts.rubric import build_prompt_rubric_json
from app.prompts.evaluation import build_prompt_submission_evaluation
from app.config.log_config import logger
from app.db.init_db import SessionLocal
from app.models.rubric import Rubric
import json
from app.models.evaluation import Evaluation
from app.db.init_db import SessionLocal
from app.prompts.rubric import (
    build_prompt_ocr_with_JSON_formatting
)
from app.prompts.evaluation import (
    build_prompt_evaluation_ocr
)

def load_rubric_node(state: dict) -> dict:
    rubric_id = state.get("rubric_id")

    update_status(state["evaluation_id"], "Fetching rubric data")

    db = SessionLocal()

    try:

        rubric = db.query(Rubric).filter(Rubric.id == rubric_id).first()

        if not rubric:
            raise ValueError("Rubric not found")

        state["rubric_json"] = rubric.rubric_json
        state["rubric_images"] = json.loads(rubric.rubric_path or "[]")

        return state

    finally:
        db.close()

def ocr_node(state: dict) -> dict:
    """
    Perform OCR on rubric and submission images.
    """
    try:
        logger.info("Starting OCR node", extra={"state_keys": list(state.keys())})

        evaluation_id = state.get("evaluation_id")
        if evaluation_id:
            update_status(evaluation_id, "Extracting data from student submission")

        # Rubric OCR
        if not state.get("rubric_id") and state.get("rubric_images"):
            logger.info(
                "Starting Rubric OCR",
                extra={
                    "rubric_images_count":
                    len(state["rubric_images"])
                }
            )
            prompt = build_prompt_ocr_with_JSON_formatting()
            result = extract_ocr(
                image_paths=state.get("rubric_images"),
                prompt=prompt
            )
            if result.get("ocr_text"):
                state["rubric_text"] = result["ocr_text"]

            if result.get("table_html"):
                state["rubric_html"] = result["table_html"]

            if result.get("llm_output"):
                state["rubric_json"] = result["llm_output"]
                logger.debug("Rubric OCR completed", extra={"rubric_json": state["rubric_json"]})

        # Submission OCR
        if state.get("submission_images"):
            logger.info("Starting Submission OCR", extra={"state_keys": list(state.keys())})
            prompt = build_prompt_evaluation_ocr()
            result = extract_ocr(
                image_paths=state["submission_images"],
                prompt=prompt,
                output_format="txt"
            )
            if result.get("llm_output"):
                state["submission_text"] = result["llm_output"]
                logger.debug("Submission OCR completed", extra={"submission_text_preview": state["submission_text"][:200]})

        logger.info("OCR node completed", extra={"state_keys": list(state.keys())})
        return state

    except Exception as e:
        logger.exception("OCR node failed", extra={"state_keys": list(state.keys())})
        raise


def merge_input_node(state: dict) -> dict:

    try:

        if not state.get("rubric_id"):
            state["rubric_text"] = (
                state.get("rubric_text")
                or state.get("ocr_rubric")
            )

        state["submission_text"] = (
            state.get("submission_text")
            or state.get("ocr_submission")
        )

        logger.info(
            "Merge input node completed",
            extra={
                "rubric_present": bool(state.get("rubric_text")),
                "submission_present": bool(state.get("submission_text"))
            }
        )

        return state

    except Exception:

        logger.exception(
            "Merge input node failed",
            extra={"state_keys": list(state.keys())}
        )
        raise

def grading_node(state: dict) -> dict:
    """
    Run grading LLM on rubric text to generate rubric JSON.
    """
    try:
        rubric_id = state.get("rubric_id")

        if rubric_id:
            if not state.get("rubric_json"):
                raise ValueError("rubric_json missing for rubric_id flow")

            logger.info("Using DB rubric_json for grading")
            return state 

        if state.get("rubric_json"):
            return state

        rubric = state.get("rubric_text")
        rubric_html = state.get("rubric_html","")
        if not rubric:
            raise ValueError("No rubric text available for grading node")

        prompt = build_prompt_rubric_json(rubric, rubric_html)
        result = run_llm(prompt)
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except:
                raise ValueError("Invalid rubric JSON from LLM")

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
        print(state)

        evaluation_id = state.get("evaluation_id")
        if evaluation_id:
            update_status(evaluation_id, "Extracting data from student submission")

        rubric_json = state.get("rubric_json")

        if isinstance(rubric_json, str):
            rubric_json = json.loads(rubric_json)
        
        submission_text = state.get("submission_text")

        if not rubric_json or not submission_text:
            raise ValueError("Rubric JSON or submission text missing for evaluation node")

        prompt = build_prompt_submission_evaluation(rubric_json, submission_text)
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


def update_status(evaluation_id, status):
    db = SessionLocal()
    try:
        eval_obj = db.query(Evaluation).get(evaluation_id)
        if eval_obj:
            eval_obj.status = status
            db.commit()
    finally:
        db.close()