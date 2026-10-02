import sqlite3

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from Backend.database.db import create_user, find_user
from Backend.security import (
    create_token,
    hash_password,
    verify_password,
)


router = APIRouter(prefix="/account", tags=["Account"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register_user(data: RegisterRequest):
    if len(data.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters."
        )

    if find_user(data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    try:
        password_hash = hash_password(data.password)

        user_id = create_user(
            data.email,
            password_hash
        )

        token = create_token(user_id)

        return {
            "message": "Account created successfully.",
            "token": token,
            "user_id": user_id
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )


@router.post("/login")
def login_user(data: LoginRequest):
    user = find_user(data.email)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = create_token(user["id"])

    return {
        "message": "Login successful.",
        "token": token,
        "user_id": user["id"],
        "email": user["email"]
    }