from fastapi import FastAPI
from app.routes import grade, auth, rubric, user
from app.db.init_db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.models.user import User  
from app.models.evaluation import Evaluation  
from app.models.rubric import Rubric  
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles

load_dotenv()

Base.metadata.create_all(bind=engine)
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(grade.router, prefix="/api", tags=["Grading"])
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authenication"])
app.include_router(rubric.router, prefix="/api", tags=["Rubric"])

@app.get("/")
def root():
    return {"status": "Backend running"}