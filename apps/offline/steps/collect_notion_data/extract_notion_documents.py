from typing_extensions import Annotated
from zenml import step, get_step_context

from offline.domain import Document, DocumentMetadata
from offline.infrastructure.notion import NotionDocumentClient

@step
def extract_notion_documents(documents_metadata: list[DocumentMetadata]) -> Annotated[list[Document], "notion_documents"]:
    """Extract content from multiple Notion documents.

    Args:
        documents_metadata: List of document metadata to extract content from.

    Returns:
        list[Document]: List of documents with their extracted content.
    """

    client = NotionDocumentClient()
    documents = []
    for document_metadata in documents_metadata:
        documents.append(client.extract_document(document_metadata))

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="notion_documents",
        metadata={
            "len_documents": len(documents)
        },
    )

    return documents