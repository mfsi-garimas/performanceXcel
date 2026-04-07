from fastapi import FastAPI
from app.routes import grade, rubric, users

app = FastAPI()

app.include_router(grade.router, prefix="/grade", tags=["Grading"])
app.include_router(rubric.router, prefix="/rubric", tags=["Rubric"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"status": "Backend running"}