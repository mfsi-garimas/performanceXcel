from pydantic import BaseModel

class UpdateEvaluationRequest(BaseModel):
    student_name: str