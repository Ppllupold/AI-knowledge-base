"""
User entity — pure domain model.

Rules:
  - No FastAPI, Motor, or Pydantic imports here.
  - Use Python dataclasses or plain classes.
  - Encode domain invariants as methods (e.g. is_active).

TODO (you implement):
  Fill in the fields. Think: what does the domain know about a User?
  Hint: id, email, hashed_password, is_active, created_at.
  Should User know its own password? Or only a hash? Why?
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class User:
    email: str
    hashed_password: str
    id: UUID = field(default_factory=uuid4)
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def deactivate(self) -> None:
        self.is_active = False
