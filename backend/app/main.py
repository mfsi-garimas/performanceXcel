from fastapi import FastAPI
from app.llm.llm_client import generate

app = FastAPI()

@app.get("/")
def root():
    print(generate("Evaluate this text: The student wrote a good essay"))
    return {"status": "Backend running"}