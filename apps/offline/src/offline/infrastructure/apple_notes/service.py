from pathlib import Path
from typing import Generic, Type, TypeVar
import sqlite3

from loguru import logger
from pydantic import BaseModel
from markdownify import markdownify

from offline.domain import Document

T = TypeVar("T", bound=BaseModel)

class AppleNotesDBService(Generic[T]):
    """Client for interacting with Apple Notes
    """

    def __init__(
        self,
        model: Type[T],
        notes_db_path: Path
    ) -> None:
        self.model = model
        self.notes_db_path = notes_db_path

        try:
            self.conn = sqlite3.connect(self.notes_db_path)
        except Exception as e:
            logger.error(f"Failed to initialize AppleNotesDBService {e}")

        logger.info(
            f"Connected to Apple Notes DB instance:\n notes_db_path: {notes_db_path}"
        )

    def __enter__(self) -> "AppleNotesDBService":
        """Enable context manager support

        Returns:
            AppleNotesDBService: The current instance.
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close AppleNotes SQL connection when exiting context.

        Args:
            exc_type: Type of exception that occurred, if any.
            exc_val: Exception instance that occurred, if any.
            exc_tb: Traceback of exception that occurred, if any.
        """

        self.close()
    
    def fetch_documents(self) -> Document:
        """Extract content from a Apple Notes database
        """

        try:
            query = "SELECT id, title, body, created, updated FROM notes"
            cursor = self.conn.cursor()
            cursor.execute(query)
            documents = list(cursor.fetchall())
            logger.debug(f"Fetched {len(documents)} documents with query: {query}")
            return self.__parse_documents(documents)
        except Exception as e:
            logger.error(f"Error fetching documents: {e}")
            raise

    def __parse_documents(self, documents: list[dict]) -> list[T]:
        """Convert Apple Notes documents to Pydantic model instances.
        """
        
        parsed_documents = []
        for doc in documents:
            note_to_doc= {
                "id": doc[0].split('/')[-1],
                "content": markdownify(doc[2]),
                "metadata": {
                    "id": doc[0],
                    "url": None,
                    "title": doc[1],
                    "properties": {
                        "created": doc[3],
                        "updated": doc[4]
                    }
                }
            }
            parsed_doc = self.model.model_validate(note_to_doc)
            parsed_documents.append(parsed_doc)

        return parsed_documents
        
    def close(self) -> None:
        """Close the AppleNotes connection.

        This method should be called when the service is no longer needed
        to properly release resources, unless using the context manager.
        """

        self.conn.close()
        logger.debug("Closed AppleNotes connection.")
