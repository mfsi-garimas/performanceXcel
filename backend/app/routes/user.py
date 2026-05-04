from app.services.file_service import (
    save_file,
    process_file,
    clean_upload_dir
)
from app.models.user import User
import json, os, shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from app.db.init_db import SessionLocal
from app.config.log_config import logger
from app.schemas.user import UserRequest, UserUpdateRequest, UserRole
from app.utils.jwt_handler import verify_token
from app.utils.security import hash_password

router = APIRouter()


@router.post("/create-user")
async def create_user(
    payload: UserRequest,
    user_email: str = Depends(verify_token)
):
    db = None

    try:
        db = SessionLocal()

        current_user = db.query(User).filter(User.email == user_email).first()

        if current_user.role != UserRole.ADMIN.value:
            raise HTTPException(status_code=403, detail="Invalid access")

        existing_user = (
            db.query(User)
            .filter(User.email == payload.email)
            .first()
        )

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = User(
            username=payload.username,
            email=payload.email,
            hashed_password=hash_password(payload.password), 
            role=payload.role.value.upper() 
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "status": "success",
            "message": "User created successfully",
            "data": {
                "id": new_user.id,
                "email": new_user.email,
                "role": new_user.role
            }
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Failed to create user")
        raise HTTPException(status_code=500, detail="Failed to create user")

    finally:
        if db:
            db.close()


@router.delete("/remove-user/{user_id}")
async def delete_rubric(
    user_id: int,
    user_email: str = Depends(verify_token)
):
    db = None

    try:
        db = SessionLocal()

        current_user = db.query(User).filter(User.email == user_email).first()

        if current_user.role != UserRole.ADMIN.value:
            raise HTTPException(status_code=403, detail="Invalid access")

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(status_code=404, detail="User not found")


        db.delete(user)
        db.commit()

        return {
            "status": "success",
            "message": "User deleted successfully"
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Failed to delete user")
        raise HTTPException(status_code=500, detail="Failed to delete user")

    finally:
        if db:
            db.close()

@router.put("/update-user/{user_id}")
async def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    user_email: str = Depends(verify_token)
):
    db = None

    try:
        db = SessionLocal()

        current_user = db.query(User).filter(User.email == user_email).first()

        if current_user.role != UserRole.ADMIN.value:
            raise HTTPException(status_code=403, detail="Invalid access")

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = payload.dict(exclude_unset=True)

        if "username" in update_data:
            user.username = update_data["username"]

        if "email" in update_data:
            user.email = update_data["email"]

        if "password" in update_data:
            user.hashed_password = hash_password(update_data["password"])

        if "role" in update_data:
            user.role = update_data["role"]

        db.commit()
        db.refresh(user)

        return {
            "status": "success",
            "message": "User updated successfully"
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Failed to update user")
        raise HTTPException(status_code=500, detail="Failed to update user")

    finally:
        if db:
            db.close()

@router.get("/get-users")
async def get_users(user_email: str = Depends(verify_token)):
    db = None

    try:
        db = SessionLocal()

        current_user = db.query(User).filter(User.email == user_email).first()

        if current_user.role != UserRole.ADMIN.value:
            raise HTTPException(status_code=403, detail="Invalid access")

        users = db.query(User).all()

        response = []
        for user in users:
            response.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "created_date": user.created_date
            })

        return {
            "status": "success",
            "count": len(response),
            "data": response
        }

    except Exception:
        logger.exception("Failed to fetch users")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

    finally:
        if db:
            db.close()

@router.get("/get-user")
async def get_user_by_id(user_email: str = Depends(verify_token)):
    db = None

    try:
        db = SessionLocal()

        current_user = db.query(User).filter(User.email == user_email).first()

        response = []
        response.append({
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "role": current_user.role
        })

        return {
            "status": "success",
            "count": len(response),
            "data": response
        }

    except Exception:
        logger.exception("Failed to fetch user")
        raise HTTPException(status_code=500, detail="Failed to fetch user")

    finally:
        if db:
            db.close()