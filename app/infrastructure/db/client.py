"""
MongoDB connection lifecycle.

Why Motor?
  Motor is the official async MongoDB driver. It integrates cleanly with
  asyncio and FastAPI. Beanie (ODM) is an option but adds coupling between
  your domain models and MongoDB schema — we avoid that here.

Motor client is created once at startup and stored on app.state.
This is the standard FastAPI pattern for shared resources.

TODO (you implement):
  connect_to_mongo() → create AsyncIOMotorClient, store on app.state
  close_mongo_connection() → close the client
  get_database() → dependency that returns the db from app.state

Important: Motor clients are thread-safe and should NOT be created per-request.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

_client: AsyncIOMotorClient | None = None


async def connect_to_mongo() -> None:
    global _client
    _client = AsyncIOMotorClient(settings.mongodb_url)
    await _client.admin.command("ping")


async def close_mongo_connection() -> None:
    if _client:
        _client.close()


def get_database() -> AsyncIOMotorDatabase:
    if _client is None:
        raise RuntimeError("MongoDB client is not initialized. Call connect_to_mongo() first.")
    return _client[settings.mongodb_db_name]
