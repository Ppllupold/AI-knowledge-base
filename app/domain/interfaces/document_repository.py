from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.document import Document, DocumentStatus


class IDocumentRepository(ABC):
    @abstractmethod
    async def create(self, document: Document) -> Document: ...

    @abstractmethod
    async def get_by_id(self, document_id: UUID) -> Document | None: ...

    @abstractmethod
    async def list_by_collection(
        self,
        collection_id: UUID,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Document]: ...

    @abstractmethod
    async def update_status(
        self,
        document_id: UUID,
        status: DocumentStatus,
        *,
        chunk_count: int | None = None,
        error_message: str | None = None,
    ) -> None: ...

    @abstractmethod
    async def delete(self, document_id: UUID) -> None: ...
