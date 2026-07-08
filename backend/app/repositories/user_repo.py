"""
Data access layer for the `users` collection.
"""
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

COLLECTION = "users"


async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> dict[str, Any] | None:
    return await db[COLLECTION].find_one({"email": email})


async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> dict[str, Any] | None:
    if not ObjectId.is_valid(user_id):
        return None
    return await db[COLLECTION].find_one({"_id": ObjectId(user_id)})


async def create_user(db: AsyncIOMotorDatabase, name: str, email: str, hashed_password: str) -> dict[str, Any]:
    doc = {
        "name": name,
        "email": email,
        "hashed_password": hashed_password,
        "created_at": datetime.now(timezone.utc),
        "is_active": True,
    }
    result = await db[COLLECTION].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


def serialize_user(user: dict[str, Any]) -> dict[str, Any]:
    """Convert a Mongo user document into a JSON-serializable public dict."""
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
    }
