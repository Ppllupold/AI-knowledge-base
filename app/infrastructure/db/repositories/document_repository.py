"""
MongoDocumentRepository — TODO (you implement after UserRepository).

MongoDB collection: "documents"
"""
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorDatabase
from uuid import UUID

from app.domain.entities.document import Document, DocumentStatus
from app.domain.interfaces.document_repository import IDocumentRepository


class MongoDocumentRepository(IDocumentRepository):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection = db["documents"]

    async def create(self, document: Document) -> Document:
        await self._collection.insert_one(self._to_document(document))
        return document

    async def get_by_id(self, document_id: UUID) -> Document | None:
        doc = await self._collection.find_one({"_id": str(document_id)})
        if not doc:
            return None
        return self._from_document(dict(doc))

    async def list_by_collection(self, collection_id: UUID, *, skip: int = 0, limit: int = 20) -> list[Document]:
        cursor = self._collection.find({"collection_id": str(collection_id)}).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [self._from_document(dict(doc)) for doc in docs]

    async def update_status(self, document_id: UUID, status: DocumentStatus, *, chunk_count: int | None = None,
                            error_message: str | None = None) -> None:
        fields = {"status": status, "updated_at": datetime.now(timezone.utc)}
        if chunk_count is not None:
            fields["chunk_count"] = chunk_count
        if error_message is not None:
            fields["error_message"] = error_message
        await self._collection.update_one({"_id": str(document_id)}, {"$set": fields})

    async def delete(self, document_id: UUID) -> None:
        await self._collection.delete_one({"_id": str(document_id)})

    def _to_document(self, document: Document) -> dict:
        return {
            "title": document.title,
            "owner_id": str(document.owner_id),
            "collection_id": str(document.collection_id),
            "filename": document.filename,
            "content_type": document.content_type,
            "_id": str(document.id),
            "status": document.status,
            "chunk_count": document.chunk_count,
            "error_message": document.error_message,
            "created_at": document.created_at,
            "updated_at": document.updated_at,
        }

    def _from_document(self, document: dict) -> Document:
        return Document(
            title=document["title"],
            owner_id=UUID(document["owner_id"]),
            collection_id=UUID(document["collection_id"]),
            filename=document["filename"],
            content_type=document["content_type"],
            id=UUID(document["_id"]),
            status=DocumentStatus(document["status"]),
            chunk_count=document["chunk_count"],
            error_message=document["error_message"],
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )
