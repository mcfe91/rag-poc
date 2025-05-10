local-zenml-server-up:
	OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES uv run zenml login --local

local-zenml-server-stop:
	uv run zenml logout --local

collect-notion-data-pipeline:
	uv run python -m tools.run --run-collect-notion-data-pipeline --no-cache

make etl-pipeline:
	uv run python -m tools.run --run-etl-pipeline --no-cache