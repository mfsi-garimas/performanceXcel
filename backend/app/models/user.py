from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.db.init_db import Base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.core.enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    reset_token_hash = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)
    role = Column(String, default=UserRole.TEACHER.value)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    evaluations = relationship("Evaluation", back_populates="user")
    rubrics = relationship("Rubric", back_populates="user")