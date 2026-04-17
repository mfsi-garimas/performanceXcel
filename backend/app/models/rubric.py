from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.init_db import Base
from datetime import datetime

class Rubric(Base):
    __tablename__ = "rubrics"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rubric_title = Column(String, nullable=False)
    rubric_path = Column(String, nullable=False)
    rubric_json = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="rubrics")