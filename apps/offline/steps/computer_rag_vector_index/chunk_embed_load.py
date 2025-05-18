from zenml import step

from offline.domain.document import Document
from offline.application.rag import get_retriever
from offline.application.rag.retrievers import RetrieverType
from offline.application.rag.embeddings import EmbeddingModelType

@step
def chunk_embed_load(
    documents: list[Document],
    collection_name: str,
    processing_batch_size: int,
    processing_max_workers: int,
    retriever_type: RetrieverType,
    embedding_model_id: str,
    embedding_model_type: EmbeddingModelType,
    embedding_model_dim: int,
    chunk_size: int,
    contextual_summarization_type: SummarizationType = "none",
    contextual_agent_model_id: str | None = None,
    contextual_agent_max_characters: int | None = None,
    mock: bool = False,
    device: str = "cpu",
) -> None:
    """Process documents by chunking, embedding, and loading into MongoDB.

    Args:
        documents: List of documents to process.
        collection_name: Name of MongoDB collection to store documents.
        processing_batch_size: Number of documents to process in each batch.
        processing_max_workers: Maximum number of concurrent processing threads.
        retriever_type: Type of retriever to use for document processing.
        embedding_model_id: Identifier for the embedding model.
        embedding_model_type: Type of embedding model to use.
        embedding_model_dim: Dimension of the embedding vectors.
        chunk_size: Size of text chunks for splitting documents.
        contextual_summarization_type: Type of summarization to apply. Defaults to "none".
        contextual_agent_model_id: ID of the model used for contextual summarization. Defaults to None.
        contextual_agent_max_characters: Maximum characters for contextual summarization. Defaults to None.
        mock: Whether to use mock processing. Defaults to False.
        device: Device to run embeddings on ('cpu' or 'cuda'). Defaults to 'cpu'.
    """

    retriever = get_retriver()
