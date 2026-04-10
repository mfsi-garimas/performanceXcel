from fastapi import FastAPI
from app.routes import grade, rubric, users, auth
from app.db.init_db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.models.user import User  
from app.models.evaluation import Evaluation  
from dotenv import load_dotenv
import os

load_dotenv()

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(grade.router, prefix="/grade", tags=["Grading"])
app.include_router(auth.router, prefix="/auth", tags=["AUTH"])

# app.include_router(rubric.router, prefix="/rubric", tags=["Rubric"])
# app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"status": "Backend running"}