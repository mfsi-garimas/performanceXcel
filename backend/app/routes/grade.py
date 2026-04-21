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
    process_file,
    clean_upload_dir
)
from app.models.evaluation import Evaluation
from app.db.init_db import SessionLocal
from datetime import datetime, timedelta
from app.utils.jwt_handler import verify_token

router = APIRouter()
graph = build_graph()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/get-all-evaluations")
async def get_all_evaluations(user_email: str = Depends(verify_token)):
    db = None

    try:
        db = SessionLocal()

        user_id = 1  

        evaluations = db.query(Evaluation).filter(Evaluation.user_id == user_id).all()

        response = []
        for e in evaluations:
            response.append({
                "id": e.id,
                "evaluation": e.evaluation,
                "student_submission": e.student_submission,
                "created_date": e.created_date,

                "rubric": {
                    "title": e.rubric.title if e.rubric else None,
                    "rubric_json": e.rubric.rubric_json if e.rubric else None,
                    "rubric_path": e.rubric.rubric_path if e.rubric else None,
                }
            })

        return {
            "status": "success",
            "count": len(response),
            "data": response
        }

    except Exception:
        logger.exception("Failed to fetch rubrics")
        raise HTTPException(status_code=500, detail="Failed to fetch rubrics")

    finally:
        if db:
            db.close()

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
            submission_images = process_file(submission_path,"submission","required")

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
            rubric_id=rubric_id,
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
            clean_upload_dir()
        except Exception:
            logger.warning("Failed to clean uploads directory")