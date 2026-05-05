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
from fastapi.responses import StreamingResponse
import asyncio
from app.models.user import User

router = APIRouter()
graph = build_graph()

def send(stage: str, message: str = None, data: dict = None):
    payload = {
        "stage": stage
    }
    if message:
        payload["message"] = message
    if data:
        payload["data"] = data

    return json.dumps(payload) + "\n"

@router.post("/add-rubric")
async def create_rubric(
    rubric_title: str = Form(...),
    rubric_file: UploadFile = File(...),
    user_email: str = Depends(verify_token)
):
    async def event_stream():
        state = {}
        db = None

        try:
            yield send("upload_started", "Uploading file...")

            await asyncio.sleep(0)

            rubric_path = await asyncio.to_thread(
                save_file, rubric_file, "rubric-images"
            )

            yield send("file_saved", "Rubric file saved...")
            await asyncio.sleep(0)

            rubric_images = await asyncio.to_thread(
                process_file, rubric_path, "rubric-images", "required"
            )
            await asyncio.sleep(0)

            state["rubric_images"] = rubric_images

            yield send("generating_rubric", "Rubric Processing started...")
            await asyncio.sleep(0)

            result = await asyncio.to_thread(graph.invoke, state)

            rubric_json_data = result.get("rubric_json")
            if not rubric_json_data:
                yield send("error", "Rubric JSON generation failed")
                return

            yield send("saving_to_db", "Saved to db...")
            await asyncio.sleep(0)

            db = SessionLocal()

            current_user = db.query(User).filter(User.email == user_email).first()

            new_rubric = Rubric(
                user_id=current_user.id,
                rubric_json=json.dumps(rubric_json_data),
                rubric_path=json.dumps(rubric_images),
                rubric_title=rubric_title
            )

            db.add(new_rubric)
            db.commit()
            db.refresh(new_rubric)

            yield send(
                "completed",
                "Rubric uploaded successfully",
                data=rubric_json_data
            )

        except Exception as e:
            yield send("error", str(e))

        finally:
            if db:
                db.close()
            # clean_upload_dir()

    return StreamingResponse(event_stream(), media_type="text/plain")

@router.get("/get-rubrics")
async def get_rubrics(user_email: str = Depends(verify_token)):
    db = None

    try:
        db = SessionLocal()

        current_user = db.query(User).filter(User.email == user_email).first()

        user_id = current_user.id

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

        current_user = db.query(User).filter(User.email == user_email).first()

        user_id = current_user.id

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