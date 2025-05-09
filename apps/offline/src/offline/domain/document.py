from pydantic import BaseModel

class DocumentMetadata(BaseModel):
    id: str
    url: str
    title: str
    properties: dict