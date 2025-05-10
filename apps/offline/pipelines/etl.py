from pathlib import Path

from loguru import logger
from zenml import pipeline

from steps.infrastructure import (
    read_documents_from_disk
)

@pipeline
def etl(
    data_dir: Path
) -> None:
    notion_data_dir = data_dir / "notion"
    logger.info(f"Reading notion data from {notion_data_dir}")

    documents = read_documents_from_disk(
        data_directory=notion_data_dir, nesting_level=1
    )