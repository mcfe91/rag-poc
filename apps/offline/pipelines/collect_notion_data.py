from pathlib import Path

from zenml import step, pipeline

from steps.collect_notion_data import extract_notion_documents_metadata

@pipeline
def collect_notion_data(database_ids: list[str], data_dir: Path, to_s3: bool = False) -> None:
    for index, database_id in enumerate(database_ids):
        documents_metadata = extract_notion_documents_metadata(database_id=database_id)
        print(documents_metadata)

