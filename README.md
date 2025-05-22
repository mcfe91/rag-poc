# Usage: #

## Add .env files: ##
### /offline ###
`NOTION_SECRET_KEY=`
`OPENAI_MODEL_ID=`
`OPENAI_API_KEY=`
`HUGGINGFACE_ACCESS_TOKEN=`
`HUGGINGFACE_DEDICATED_ENDPOINT=`

### /online ###
`OPENAI_MODEL_ID=`
`OPENAI_API_KEY=`
`HUGGINGFACE_ACCESS_TOKEN=`
`HUGGINGFACE_DEDICATED_ENDPOINT=`
`COMET_API_KEY=`

## MongoDB ##
`make local-docker-infrastructure-up`

## Set pipeline configs ##
`./offline/configs/*.yaml`

## Collect raw data ##
`make collect-notion-data-pipeline`
`make collect-apple-notes-data-pipeline`

## Extract, Transform, Load pipeline ##
`make etl-notion-pipeline`
`make etl-apple-notes-pipeline`

## Generate custom dataset ##
`make generate-dataset-pipeline`

## RAG Ingestion - Chunk, embed, load ##
`make compute-rag-vector-index-openai-parent-pipeline`

## Run agentic rag - query CLI ##
`make run_agent_query`

## Run agentic rag - GradioUI Chat ##
`make run_agent_app`

## Evaluate RAG system ##
`make evaluate_agent`
