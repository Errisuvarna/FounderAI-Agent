"""
MongoDB connection management using Motor (async driver).
Exposes a single AsyncIOMotorDatabase instance shared across the app lifecycle.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class MongoDatabase:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None


mongo = MongoDatabase()


async def connect_to_mongo() -> None:
    """Initialize the MongoDB client and create required indexes."""
    mongo.client = AsyncIOMotorClient(settings.MONGODB_URI)
    mongo.db = mongo.client[settings.MONGODB_DB_NAME]

    # Indexes
    await mongo.db["users"].create_index("email", unique=True)
    await mongo.db["startups"].create_index("user_id")
    await mongo.db["blueprints"].create_index("startup_id", unique=True)


async def close_mongo_connection() -> None:
    """Close the MongoDB client connection on app shutdown."""
    if mongo.client:
        mongo.client.close()


def get_db() -> AsyncIOMotorDatabase:
    """FastAPI dependency accessor for the shared database instance."""
    if mongo.db is None:
        raise RuntimeError("MongoDB has not been initialized yet.")
    return mongo.db
