from pathlib import Path

from smolagents import MultiStepAgent

from .tools import (
    MongoDBRetrieverTool
)

def get_agent(retriever_config_path: Path) -> "AgentWrapper":
    agent = AgentWrapper.build_from_smolagents(
        retriever_config_path=retriever_config_path
    )

    return agent

class AgentWrapper():
    def __init__(self, agent: MultiStepAgent) -> None:
        self.__agent = agent

    @classmethod
    def build_from_smolagents(cls, retriever_config_path: Path) -> "AgentWrapper":
        retriever_tool = MongoDBRetrieverTool(config_path=retriever_config_path)
        