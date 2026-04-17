import os
import shutil
from app.config.log_config import logger
import json
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends

from app.graph.build_graph import build_graph
from app.services.file_service import (
    get_file_extension,
    pdf_to_images,
    docx_to_images,
    save_file,
    process_file
)
from app.models.evaluation import Evaluation
from app.db.init_db import SessionLocal
from datetime import datetime, timedelta
from app.utils.jwt_handler import verify_token

router = APIRouter()
graph = build_graph()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/grade")
async def grade_submission(
    rubric_id: int = Form(...),
    submission_file: UploadFile = File(None),
    user_email: str = Depends(verify_token)
):
    state = {}

    try:
        if not (rubric_id):
            raise HTTPException(status_code=400, detail="Rubric is required")

        if not (submission_file):
            raise HTTPException(status_code=400, detail="Submission input is required")

        state["rubric_id"] = rubric_id

        if submission_file:
            logger.info("Processing submission file", extra={"submission_file_name": submission_file.filename})

            submission_path = save_file(submission_file, "submission")
            submission_images = process_file(submission_path)

            state["submission_images"] = submission_images

        logger.debug("Initial state prepared", extra={"keys": list(state.keys())})

        result = graph.invoke(state)

        evaluation_json = json.dumps(result["final_output"])

        rubric_value = json.dumps(result["rubric_images"])
        student_submission_value = json.dumps(result["submission_images"])

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
                for item in os.listdir(UPLOAD_DIR):
                    item_path = os.path.join(UPLOAD_DIR, item)

                    if item == "rubric-images":
                        continue

                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
        except Exception:
            logger.warning("Failed to clean uploads directory")