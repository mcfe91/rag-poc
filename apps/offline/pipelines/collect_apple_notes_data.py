from pathlib import Path

from loguru import logger
from zenml import pipeline

from steps.collect_apple_notes_data import extract_apple_notes_documents
from steps.infrastructure import save_documents_to_disk


@pipeline
def collect_apple_notes_data(notes_db_path: Path, data_dir: Path, to_s3: bool = False) -> None:
    apple_notes_data_dir = data_dir / "apple_notes"
    apple_notes_data_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Collecting pages from database '{notes_db_path}'")
    documents_data = extract_apple_notes_documents(notes_db_path=notes_db_path)

    result = save_documents_to_disk(documents=documents_data, output_dir=apple_notes_data_dir / "database")