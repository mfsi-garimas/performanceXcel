from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.init_db import SessionLocal
from app.models.user import User
from app.utils.security import verify_password
from app.utils.jwt_handler import create_access_token
import secrets
from app.utils.limiter import limiter
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from datetime import datetime, timedelta
from app.utils.security import hash_password, hash_token
from app.schemas.auth import LoginRequest, ForgetPasswordRequest
from app.utils.email import send_email

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token}


@router.post("/forgot-password")
def forgot_password(data: ForgetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="No user found")

    raw_token = secrets.token_urlsafe(32)
    token_hash = hash_token(raw_token)

    user.reset_token_hash = token_hash
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)
    db.commit()

    reset_link = f"http://localhost:5173/reset-password?token={raw_token}"

    print(reset_link)

    # send_email(user.email, reset_link)

    return {"message": "Reset link sent"}

@router.post("/reset-password")
def reset_password(data: dict, db: Session = Depends(get_db)):
    token_hash = hash_token(data["token"])

    user = db.query(User).filter(
        User.reset_token_hash == token_hash
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    if user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user.hashed_password = hash_password(data["password"])
    user.reset_token_hash = None
    user.reset_token_expiry = None

    db.commit()

    return {"message": "Password updated"}