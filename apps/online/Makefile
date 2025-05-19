RETRIEVER_CONFIG ?= configs/compute_rag_vector_index_openai_parent.yaml

check-config:
	@if [ ! -f "$(RETRIEVER_CONFIG)" ]; then \
		echo "Error: Retriever config file '$(RETRIEVER_CONFIG)' does not exist"; \
		exit 1; \
	else \
		echo "Found retriever config file at '$(RETRIEVER_CONFIG)'"; \
	fi

run_agent_query: check-config
	uv run python -m tools.app --retriever-config-path=$(RETRIEVER_CONFIG) --query "What's the difference between vector databases and vector indices?"

run_agent_app: check-config
	uv run python -m tools.app --retriever-config-path=$(RETRIEVER_CONFIG) --ui