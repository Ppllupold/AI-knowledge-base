"""
IUserRepository — the contract that infrastructure must satisfy.

Why an interface here?
  The domain layer needs to persist users, but MUST NOT know about MongoDB.
  This Abstract Base Class defines WHAT operations are needed (the port).
  The infrastructure layer provides the MongoDB implementation (the adapter).

  This is the Dependency Inversion Principle:
    "High-level modules should not depend on low-level modules."
    AuthService depends on IUserRepository, NOT on MongoUserRepository.

Interview question you should be able to answer:
  "How does this pattern help with testing?"
  → You can inject a FakeUserRepository in tests with no MongoDB needed.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None: ...
