"""
Profile route: GET /profile — returns the authenticated user's profile.
"""
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import UserPublic
from app.repositories.user_repo import serialize_user

router = APIRouter(tags=["profile"])


@router.get("/profile", response_model=UserPublic)
async def get_profile(current_user: dict[str, Any] = Depends(get_current_user)):
    """Return the profile of the currently authenticated user."""
    return serialize_user(current_user)
