from pydantic import BaseModel, Field

from offline import utils

class DocumentMetadata(BaseModel):
    id: str
    url: str
    title: str
    properties: dict

class Document(BaseModel):
    id: str = Field(default_factory=lambda: utils.generate_rand_hex(length=32))
    metadata: DocumentMetadata
    parent_metadata: DocumentMetadata | None = None
    content: str
    content_quality_score: float | None = None
    summary: str | None = None
    child_urls: list[str] = Field(default_factory=list)