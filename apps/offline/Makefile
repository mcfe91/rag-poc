local-zenml-server-up:
	OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES uv run zenml login --local

local-zenml-server-stop:
	uv run zenml logout --local

collect-notion-data-pipeline:
	uv run python -m tools.run --run-collect-notion-data-pipeline --no-cache

collect-apple-notes-data-pipeline:
	uv run python -m tools.run --run-collect-apple-notes-data-pipeline --no-cache

etl-notion-pipeline:
	uv run python -m tools.run --run-etl-notion-pipeline --no-cache

etl-apple-notes-pipeline:
	uv run python -m tools.run --run-etl-apple-notes-pipeline --no-cache

generate-dataset-pipeline:
	uv run python -m tools.run --run-generate-dataset-pipeline --no-cache