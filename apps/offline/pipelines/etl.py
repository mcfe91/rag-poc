from pathlib import Path

from loguru import logger
from zenml import pipeline

from steps.infrastructure import (
    read_documents_from_disk,
)
from steps.etl import (
    add_quality_score,
)

@pipeline
def etl(
    data_dir: Path,
    load_collection_name: str,
    to_s3: bool = False,
    max_workers: int = 10,
    quality_agent_model_id: str = "gpt-4o-mini",
    quality_agent_mock: bool = True,
) -> None:
    notion_data_dir = data_dir / "notion"
    logger.info(f"Reading notion data from {notion_data_dir}")

    documents = read_documents_from_disk(
        data_directory=notion_data_dir, nesting_level=1
    )

    enhanced_documents = add_quality_score(
        documents=documents,
        model_id=quality_agent_model_id,
        mock=quality_agent_mock,
        max_workers=max_workers,
    )