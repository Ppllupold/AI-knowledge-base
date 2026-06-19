"""
MongoUserRepository — concrete implementation of IUserRepository.

This class is the only place in the codebase that knows about MongoDB
collection names, document structure, and query patterns for users.

Key decisions to make (you implement):
  - How do you map between the User domain entity and a MongoDB document?
    (UUID → str? datetime handling? field naming conventions?)
  - What indexes do you create? (email should be unique)
  - How do you handle "not found" — return None or raise?
    (IUserRepository says None — follow the contract)

TODO (you implement):
  - _to_document(user: User) -> dict
  - _from_document(doc: dict) -> User
  - All CRUD methods

MongoDB collection: "users"
"""

from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.entities.user import User
from app.domain.interfaces.user_repository import IUserRepository


class MongoUserRepository(IUserRepository):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection = db["users"]

    async def create(self, user: User) -> User:
        await self._collection.insert_one(self._to_document(user))
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        user = await self._collection.find_one({"_id": str(user_id)})
        if not user:
            return None
        return self._from_document(dict(user))

    async def get_by_email(self, email: str) -> User | None:
        user = await self._collection.find_one({"email": email})
        if not user:
            return None
        return self._from_document(dict(user))

    async def update(self, user: User) -> User:
        raise NotImplementedError

    async def delete(self, user_id: UUID) -> None:
        raise NotImplementedError

    def _to_document(self, user: User) -> dict:
        return {
            "_id": str(user.id),
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }

    def _from_document(self, doc: dict) -> User:
        return User(
            id=UUID(doc["_id"]),
            email=doc["email"],
            hashed_password=doc["hashed_password"],
            is_active=doc["is_active"],
            created_at=doc["created_at"],
        )
