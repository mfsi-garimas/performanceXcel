from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.init_db import Base
from datetime import datetime

class Evaluation(Base):
    __tablename__ = "evaluation"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    evaluation = Column(String, nullable=False)
    rubric = Column(String, nullable=True)
    student_submission = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="evaluations")