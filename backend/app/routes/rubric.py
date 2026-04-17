from app.services.file_service import (
    save_file,
    process_file,
    clean_upload_dir
)
from app.models.rubric import Rubric
import json, os, shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from app.db.init_db import SessionLocal
from app.graph.build_graph import build_graph
from app.utils.jwt_handler import verify_token
from app.config.log_config import logger

router = APIRouter()
graph = build_graph()

@router.post("/add-rubric")
async def create_rubric(
    rubric_title: str = Form(...),
    rubric_file: UploadFile = File(...),
    user_email: str = Depends(verify_token)
):
    state = {}
    db = None

    try:
        logger.info("Processing rubric file", extra={
            "rubric_file_name": rubric_file.filename
        })

        rubric_path = save_file(rubric_file, "rubric-images")
        rubric_images = process_file(rubric_path, "rubric-images")

        state["rubric_images"] = rubric_images

        logger.debug("Initial state prepared", extra={
            "keys": list(state.keys())
        })

        result = graph.invoke(state)

        rubric_json_data = result.get("rubric_json")
        if not rubric_json_data:
            raise ValueError("Rubric JSON generation failed")

        rubric_json = json.dumps(rubric_json_data)
        rubric_value = json.dumps(rubric_images)

        db = SessionLocal()

        new_rubric = Rubric(
            user_id=1,  
            rubric_json=rubric_json,
            rubric_path=rubric_value,
            rubric_title=rubric_title
        )

        db.add(new_rubric)
        db.commit()
        db.refresh(new_rubric)

        logger.info("Rubric saved", extra={"rubric_id": new_rubric.id})

        return {
            "status": "success",
            "data": rubric_json_data
        }

    except HTTPException:
        raise

    except ValueError as e:
        logger.warning("Validation error", extra={"error": str(e)})
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        logger.exception("Failed to store rubric")
        raise HTTPException(status_code=500, detail="Failed to process rubric")

    finally:
        if db:
            db.close()

        clean_upload_dir(exclude={"rubric-images"})

@router.get("/get-rubrics")
async def get_rubrics(user_email: str = Depends(verify_token)):
    db = None

    try:
        db = SessionLocal()

        user_id = 1  

        rubrics = db.query(Rubric).filter(Rubric.user_id == user_id).all()

        response = []
        for r in rubrics:
            response.append({
                "id": r.id,
                "rubric_title": r.rubric_title,
                "rubric_path": r.rubric_path,
                "created_date": r.created_date
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

@router.delete("/remove-rubric/{rubric_id}")
async def delete_rubric(
    rubric_id: int,
    user_email: str = Depends(verify_token)
):
    db = None

    try:
        db = SessionLocal()

        user_id = 1  

        rubric = (
            db.query(Rubric)
            .filter(Rubric.id == rubric_id, Rubric.user_id == user_id)
            .first()
        )

        if not rubric:
            raise HTTPException(status_code=404, detail="Rubric not found")

        try:
            paths = json.loads(rubric.rubric_path or "[]")

            for p in paths:
                if os.path.exists(p):
                    os.remove(p)

        except Exception:
            logger.warning("Failed to delete rubric files from disk")

        db.delete(rubric)
        db.commit()

        return {
            "status": "success",
            "message": "Rubric deleted successfully"
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Failed to delete rubric")
        raise HTTPException(status_code=500, detail="Failed to delete rubric")

    finally:
        if db:
            db.close()