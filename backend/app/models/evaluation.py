from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.init_db import Base
from datetime import datetime

class Evaluation(Base):
    __tablename__ = "evaluation"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rubric_id = Column(Integer, ForeignKey("rubrics.id"), nullable=False, index=True)

    evaluation = Column(String, nullable=True)
    student_name = Column(String, nullable=False)
    student_submission = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="evaluations")
    rubric = relationship("Rubric", back_populates="evaluations")