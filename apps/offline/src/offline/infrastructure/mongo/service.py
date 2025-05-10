from typing import Generic, Type, TypeVar

from bson import ObjectId
from loguru import logger
from pydantic import BaseModel
from pymongo import MongoClient, errors

from offline.config import settings

T = TypeVar("T", bound=BaseModel)

class MongoDBService(Generic[T]):
    """Service class for MongoDB operations, supporting ingestion, querying, and validation.

    This class provides methods to interact with MongoDB collections, including document
    ingestion, querying, and validation operations.

    Args:
        model: The Pydantic model class to use for document serialization.
        collection_name: Name of the MongoDB collection to use.
        database_name: Name of the MongoDB database to use.
        mongodb_uri: URI for connecting to MongoDB instance.

    Attributes:
        model: The Pydantic model class used for document serialization.
        collection_name: Name of the MongoDB collection.
        database_name: Name of the MongoDB database.
        mongodb_uri: MongoDB connection URI.
        client: MongoDB client instance for database connections.
        database: Reference to the target MongoDB database.
        collection: Reference to the target MongoDB collection.
    """

    def __init__(
        self,
        model: Type[T],
        collection_name: str,
        database_name: str = settings.MONGODB_DATABASE_NAME,
        mongodb_uri: str = settings.MONGODB_URI,
    ) -> None:
        """Initialize a connection to the MongoDB collection.

        Args:
            collection_name: Name of the MongoDB collection to use.
            model_class: The Pydantic model class to use for document serialization.
            database_name: Name of the MongoDB database to use.
                Defaults to value from settings.
            mongodb_uri: URI for connecting to MongoDB instance.
                Defaults to value from settings.

        Raises:
            Exception: If connection to MongoDB fails.
        """

        self.model = model
        self.collection_name = collection_name
        self.database_name = database_name
        self.mongodb_uri = mongodb_uri
        
        try:
            self.client = MongoClient(mongodb_uri, appname="offline")
            self.client.admin.command("ping")
        except Exception as e:
            logger.error(f"Failed to initialize MongoDBService: {e}")
            raise

        self.database = self.client[database_name]
        self.collection = self.database[collection_name]
        logger.info(
            f"Connected to MongoDB instance:\n URI: {mongodb_uri}\n Database: {database_name}\n Collection: {collection_name}"
        )

    def __enter__(self) -> "MongoDBService":
        """Enable context manager support

        Returns:
            MongoDBService: The current instance.
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close MongoDB connection when exiting context.

        Args:
            exc_type: Type of exception that occurred, if any.
            exc_val: Exception instance that occurred, if any.
            exc_tb: Traceback of exception that occurred, if any.
        """

        self.close()

    def clear_collection(self) -> None:
        """Remove all documents from the collection.

        This method deletes all documents in the collection to avoid duplicates
        during reingestion.

        Raises:
            errors.PyMongoError: If the deletion operation fails.
        """

        try:
            result = self.collection.delete_many({})
            logger.debug(
                f"Cleared collection. Deleted {result.deleted_count} documents."
            )
        except errors.PyMongoError as e:
            logger.error(f"Error clearing the collection: {e}")
            raise

    def ingest_documents(self, documents: list[T]) -> None:
        """Insert multiple documents into the MongoDB collection.

        Args:
            documents: List of Pydantic model instances to insert.

        Raises:
            ValueError: If documents is empty or contains non-Pydantic model items.
            errors.PyMongoError: If the insertion operation fails.
        """

        try:
            if not documents or not all(
                isinstance(doc, BaseModel) for doc in documents
            ):
                raise ValueError("Documents must be a list of Pydantic models.")
            
            dict_documents = [doc.model_dump() for doc in documents]

            for doc in dict_documents:
                doc.pop("_id", None)

            self.collection.insert_many(dict_documents)
            logger.debug(f"Inserted {len(documents)} documents into MongoDB.")
        except errors.PyMongoError as e:
            logger.error(f"Error inserting documents: {e}")
            raise

    def get_collection_count(self) -> int:
        """Count the total number of documents in the collection.

        Returns:
            Total number of documents in the collection.

        Raises:
            errors.PyMongoError: If the count operation fails.
        """
    
        try:
            return self.collection.count_documents({})
        except errors.PyMongoError as e:
            logger.error(f"Error counting documents in MongoDB: {e}")
            raise

    def close(self) -> None:
        """Close the MongoDB connection.

        This method should be called when the service is no longer needed
        to properly release resources, unless using the context manager.
        """

        self.client.close()
        logger.debug("Closed MongoDB connection.")






