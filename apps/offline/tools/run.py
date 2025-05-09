import click
from pathlib import Path
from datetime import datetime as dt

from pipelines import (
    collect_notion_data
)

@click.command(
    help="""
Main entry point for the pipeline execution. 
"""
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
@click.option(
    "--run-collect-notion-data-pipeline",
    is_flag=True,
    default=False,
    help="Whether to run the collection data from Notion pipeline.",
)

def main(
    no_cache: bool = False,
    run_collect_notion_data_pipeline: bool = False,
) -> None:
    pipeline_args: dict[str, Any] = {
        "enable_cache": not no_cache,
    }
    root_dir = Path(__file__).resolve().parent.parent
    
    if run_collect_notion_data_pipeline:
        run_args = {}
        pipeline_args["config_path"] = root_dir / "configs" / "collect_notion_data.yaml"
        assert pipeline_args["config_path"].exists(), f"Config file not found: {pipeline_args['config_path']}"
        pipeline_args["run_name"] = f"collect_notion_data_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        collect_notion_data.with_options(**pipeline_args)(**run_args)

if __name__ == "__main__":
    main()

