import os
import shutil
from app.config.log_config import logger
import json
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends

from app.graph.build_graph import build_graph
from app.services.file_service import (
    get_file_extension,
    pdf_to_images,
    docx_to_images
)
from app.models.evaluation import Evaluation
from app.db.init_db import SessionLocal
from datetime import datetime, timedelta
from app.utils.jwt_handler import verify_token

router = APIRouter()
graph = build_graph()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def process_file(file_path: str):
    try:
        ext = get_file_extension(file_path)

        if ext in ["png", "jpg", "jpeg"]:
            return [file_path]

        elif ext == "pdf":
            return pdf_to_images(file_path)

        elif ext == "docx":
            return docx_to_images(file_path)

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception:
        logger.exception("File processing failed", extra={"file_path": file_path})
        raise


def save_file(file: UploadFile, folder: str):
    try:
        dir_path = os.path.join(UPLOAD_DIR, folder)
        os.makedirs(dir_path, exist_ok=True)

        path = os.path.join(dir_path, file.filename)

        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        return path

    except Exception:
        logger.exception("File saving failed", extra={"filename": file.filename})
        raise


@router.post("/")
async def grade_submission(
    rubric_file: UploadFile = File(None),
    submission_file: UploadFile = File(None),
    user_email: str = Depends(verify_token)
):
    state = {}

    try:
        if not (rubric_file or rubric_text):
            raise HTTPException(status_code=400, detail="Rubric input is required")

        if not (submission_file or submission_text):
            raise HTTPException(status_code=400, detail="Submission input is required")

        if rubric_file:
            logger.info("Processing rubric file", extra={"rubric_file_name": rubric_file.filename})

            rubric_path = save_file(rubric_file, "rubric")
            rubric_images = process_file(rubric_path)

            state["rubric_images"] = rubric_images
        else:
            state["rubric_text"] = rubric_text

        if submission_file:
            logger.info("Processing submission file", extra={"submission_file_name": submission_file.filename})

            submission_path = save_file(submission_file, "submission")
            submission_images = process_file(submission_path)

            state["submission_images"] = submission_images
        else:
            state["submission_text"] = submission_text

        logger.debug("Initial state prepared", extra={"keys": list(state.keys())})

        result = graph.invoke(state)

        evaluation_json = json.dumps(result["final_output"])

        rubric_value = json.dumps(state["rubric_images"])
        student_submission_value = json.dumps(state["submission_images"])

        db = SessionLocal()
        new_eval = Evaluation(
            user_id=1,
            evaluation=evaluation_json,
            rubric=rubric_value,
            student_submission=student_submission_value
        )

        db.add(new_eval)
        db.commit()
        db.refresh(new_eval)

        print("Evaluation saved:", new_eval.id)
        db.close()
        print(result.get("final_output", {}))

        return {
            "status": "success",
            "data": result.get("final_output", {})
        }

    except HTTPException:
        raise

    except ValueError as e:
        logger.warning("Validation/processing error", extra={"error": str(e)})
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        logger.exception("Grade submission failed")
        raise HTTPException(status_code=500, detail="Failed to process submission")

    finally:
        try:
            if os.path.exists(UPLOAD_DIR):
                shutil.rmtree(UPLOAD_DIR)
                os.makedirs(UPLOAD_DIR, exist_ok=True)
        except Exception:
            logger.warning("Failed to clean uploads directory")