from app.core.worker import celery
from app.db.init_db import SessionLocal
from app.models.evaluation import Evaluation
from app.graph.build_graph import build_graph
from app.services.file_service import (
    process_file,
    clean_upload_dir
)
from app.config.log_config import logger
import json

graph = build_graph()

@celery.task
def process_submission(evaluation_id: int):
    db = SessionLocal()

    eval_obj = db.query(Evaluation).get(evaluation_id)
    if not eval_obj:
        return

    try:
        eval_obj.status = "processing"
        db.commit()

        file_paths = json.loads(eval_obj.student_submission)

        file_path = file_paths[0]

        state = {
            "rubric_id": eval_obj.rubric_id,
            "evaluation_id": evaluation_id,
            "submission_images": process_file(file_path, "submission", "required")
        }

        result = graph.invoke(state)

        eval_obj.evaluation = json.dumps(result["final_output"])

        eval_obj.status = "completed"

    except Exception as e:
        eval_obj.status = "failed"
    finally:
        # try:
            # clean_upload_dir()
        # except Exception:
        #     logger.warning("Failed to clean uploads directory")

        db.commit()
        db.close()
