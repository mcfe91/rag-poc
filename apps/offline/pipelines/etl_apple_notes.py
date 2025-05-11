from pathlib import Path

from loguru import logger
from zenml import pipeline

from steps.infrastructure import (
    read_documents_from_disk,
    save_documents_to_disk,
    ingest_to_mongodb
)
from steps.etl import (
    add_quality_score,
)

@pipeline
def etl_apple_notes(
    data_dir: Path,
    load_collection_name: str,
    to_s3: bool = False,
    max_workers: int = 10,
    quality_agent_model_id: str = "gpt-4o-mini",
    quality_agent_mock: bool = True,
) -> None:
    apple_data_dir = data_dir / "apple_notes"
    logger.info(f"Reading apple data from {apple_data_dir}")
    crawled_data_dir = data_dir / "apple_crawled"
    logger.info(f"Reading apple data from {crawled_data_dir}")

    documents = read_documents_from_disk(
        data_directory=apple_data_dir, nesting_level=1
    )

    enhanced_documents = add_quality_score(
        documents=documents,
        model_id=quality_agent_model_id,
        mock=quality_agent_mock,
        max_workers=max_workers,
    )

    save_documents_to_disk(documents=enhanced_documents, output_dir=crawled_data_dir)

    ingest_to_mongodb(
        models=enhanced_documents,
        collection_name=load_collection_name,
        clear_collection=True,
    )