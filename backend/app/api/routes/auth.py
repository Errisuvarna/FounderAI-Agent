"""
Authentication routes: POST /register, POST /login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.db.mongo import get_db
from app.models.user import TokenResponse, UserLoginRequest, UserRegisterRequest
from app.repositories.user_repo import create_user, get_user_by_email, serialize_user

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Register a new user account.
    Returns access + refresh JWT tokens along with the created user profile.
    """
    existing = await get_user_by_email(db, payload.email)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    hashed = hash_password(payload.password)
    user = await create_user(db, name=payload.name, email=payload.email, hashed_password=hashed)

    user_id = str(user["_id"])
    access_token = create_access_token(subject=user_id)
    refresh_token = create_refresh_token(subject=user_id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=serialize_user(user),
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Authenticate an existing user with email + password.
    Returns access + refresh JWT tokens along with the user profile.
    """
    user = await get_user_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user_id = str(user["_id"])
    access_token = create_access_token(subject=user_id)
    refresh_token = create_refresh_token(subject=user_id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=serialize_user(user),
    )
