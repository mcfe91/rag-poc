from pathlib import Path
from typing_extensions import Annotated
from zenml import step, get_step_context

from offline.domain import Document
from offline.infrastructure.apple_notes import AppleNotesDBService

@step
def extract_apple_notes_documents(notes_db_path: Path) -> Annotated[list[Document], "apple_notes_documents"]:
    """Extract content from Apple Notes.

    Args:
        documents_metadata: List of document metadata to extract content from.

    Returns:
        list[Document]: List of documents with their extracted content.
    """
    
    with AppleNotesDBService(model=Document, notes_db_path=notes_db_path) as service:
        documents = service.fetch_documents()

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="apple_notes_documents",
        metadata={
            "len_documents": len(documents)
        },
    )
    
    return documents
