"""
Data access layer for the `startups` and `blueprints` collections.
"""
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

STARTUPS_COLLECTION = "startups"
BLUEPRINTS_COLLECTION = "blueprints"


async def create_startup(
    db: AsyncIOMotorDatabase,
    user_id: str,
    idea_title: str,
    idea_description: str,
    industry: str,
    target_market: str,
) -> dict[str, Any]:
    doc = {
        "user_id": ObjectId(user_id),
        "idea_title": idea_title,
        "idea_description": idea_description,
        "industry": industry,
        "target_market": target_market,
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = await db[STARTUPS_COLLECTION].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


async def update_startup_status(db: AsyncIOMotorDatabase, startup_id: str, status: str) -> None:
    await db[STARTUPS_COLLECTION].update_one(
        {"_id": ObjectId(startup_id)},
        {"$set": {"status": status, "updated_at": datetime.now(timezone.utc)}},
    )


async def list_startups_for_user(db: AsyncIOMotorDatabase, user_id: str) -> list[dict[str, Any]]:
    cursor = db[STARTUPS_COLLECTION].find({"user_id": ObjectId(user_id)}).sort("created_at", -1)
    return [doc async for doc in cursor]


async def get_startup_by_id(db: AsyncIOMotorDatabase, startup_id: str) -> dict[str, Any] | None:
    if not ObjectId.is_valid(startup_id):
        return None
    return await db[STARTUPS_COLLECTION].find_one({"_id": ObjectId(startup_id)})


async def save_blueprint(db: AsyncIOMotorDatabase, startup_id: str, blueprint: dict[str, Any]) -> dict[str, Any]:
    doc = {
        "startup_id": ObjectId(startup_id),
        **blueprint,
        "created_at": datetime.now(timezone.utc),
    }
    await db[BLUEPRINTS_COLLECTION].update_one(
        {"startup_id": ObjectId(startup_id)}, {"$set": doc}, upsert=True
    )
    return await db[BLUEPRINTS_COLLECTION].find_one({"startup_id": ObjectId(startup_id)})


def serialize_startup(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "user_id": str(doc["user_id"]),
        "idea_title": doc["idea_title"],
        "idea_description": doc["idea_description"],
        "industry": doc["industry"],
        "target_market": doc["target_market"],
        "status": doc["status"],
        "created_at": doc["created_at"],
    }


def serialize_blueprint(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "startup_id": str(doc["startup_id"]),
        "idea_title": doc.get("idea_title", ""),
        "executive_summary": doc.get("executive_summary", ""),
        "market_research": doc.get("market_research", {}),
        "financial_plan": doc.get("financial_plan", {}),
        "tech_architecture": doc.get("tech_architecture", {}),
        "growth_strategy": doc.get("growth_strategy", {}),
        "pitch_deck_outline": doc.get("pitch_deck_outline", {}),
        "agent_outputs": doc.get("agent_outputs", []),
        "created_at": doc["created_at"],
    }
