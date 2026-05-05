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
from app.schemas.evaluation import UpdateEvaluationRequest
from app.models.user import User
from typing import List
from app.tasks.evaluation_tasks import process_submission

router = APIRouter()
graph = build_graph()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/get-all-evaluations")
async def get_all_evaluations(user_email: str = Depends(verify_token)):
    db = None

    try:
        db = SessionLocal()

        current_user = db.query(User).filter(User.email == user_email).first()

        user_id = current_user.id 

        evaluations = db.query(Evaluation).filter(Evaluation.user_id == user_id).all()

        response = []
        for e in evaluations:
            response.append({
                "id": e.id,
                "evaluation": e.evaluation,
                "student_submission": e.student_submission,
                "student_name": e.student_name,
                "status": e.status,
                "created_date": e.created_date,

                "rubric": {
                    "title": e.rubric.rubric_title if e.rubric else None,
                    "rubric_path": e.rubric.rubric_path if e.rubric else None,
                    "rubric_id": e.rubric.id if e.rubric else None,
                }
            })

        return {
            "status": "success",
            "count": len(response),
            "data": response
        }

    except Exception:
        logger.exception("Failed to fetch evaluations")
        raise HTTPException(status_code=500, detail="Failed to fetch evaluations")

    finally:
        if db:
            db.close()

@router.post("/evaluate-submissions")
async def grade_submission(
    rubric_id: int = Form(...),
    submission_files: List[UploadFile] = File(...),
    user_email: str = Depends(verify_token)
):
    state = {}

    try:
        if not (rubric_id):
            raise HTTPException(status_code=400, detail="Rubric is required")

        if not (submission_files):
            raise HTTPException(status_code=400, detail="Submission input is required")
        
        db = SessionLocal()

        jobs = []

        current_user = db.query(User).filter(User.email == user_email).first()

        for file in submission_files:
            logger.info("Processing submission file", extra={"submission_file_name": file.filename})
            submission_path = save_file(file, "submission")

            new_eval = Evaluation(
                user_id=current_user.id,
                rubric_id=rubric_id,
                student_name=os.path.splitext(file.filename)[0],
                student_submission=json.dumps([submission_path]),
                status="pending"
            )

            db.add(new_eval)
            db.flush()

            jobs.append({
                "evaluation_id": new_eval.id,
                "file_name": file.filename
            })

        db.commit()

        for job in jobs:
            process_submission.delay(job["evaluation_id"])

        return {
            "status": "success",
            "data": jobs
        }

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.put("/update-evaluation/{eval_id}")
async def update_evaluation(
    eval_id: int,
    payload: UpdateEvaluationRequest,
    user_email: str = Depends(verify_token)
):
    db = None

    try:
        db = SessionLocal()

        current_user = db.query(User).filter(User.email == user_email).first()

        user_id = current_user.id

        evaluation = (
            db.query(Evaluation)
            .filter(Evaluation.id == eval_id, Evaluation.user_id == user_id)
            .first()
        )

        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")

        evaluation.student_name = payload.student_name

        db.commit()
        db.refresh(evaluation)

        return {
            "status": "success",
            "message": "Student name updated successfully"
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Failed to update evaluation")
        raise HTTPException(status_code=500, detail="Failed to update evaluation")

    finally:
        if db:
            db.close()

@router.post("/retry-evaluation/{eval_id}")
async def retry_evaluation(
    eval_id: int,
    user_email: str = Depends(verify_token)
):
    db = None

    try:
        db = SessionLocal()

        current_user = db.query(User).filter(User.email == user_email).first()

        evaluation = (
            db.query(Evaluation)
            .filter(Evaluation.id == eval_id, Evaluation.user_id == current_user.id)
            .first()
        )

        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")

        if evaluation.status != "failed":
            raise HTTPException(
                status_code=400,
                detail="Only failed evaluations can be retried"
            )

        evaluation.status = "pending"
        evaluation.evaluation = None  

        db.commit()

        process_submission.delay(evaluation.id)

        return {
            "status": "success",
            "message": "Retry started",
            "evaluation_id": evaluation.id
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Retry failed")
        raise HTTPException(status_code=500, detail="Retry failed")

    finally:
        if db:
            db.close()