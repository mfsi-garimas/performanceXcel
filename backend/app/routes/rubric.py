from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_rubrics():
    return {"message": "Rubric endpoint"}