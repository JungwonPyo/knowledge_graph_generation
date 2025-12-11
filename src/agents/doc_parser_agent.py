from ._agent_registry import AgentRegistry
from src.models import AgentName, Unit
from src.agents.prompts import DOC_PARSER_PROMPT
from pydantic_ai import Agent

from ._base import model

@AgentRegistry.register(AgentName.doc_parser_agent)
def create_doc_parser_agent() -> Agent:
    agent = Agent(
        name=AgentName.doc_parser_agent.value,
        model=model,
        system_prompt=DOC_PARSER_PROMPT,
        output_type=Unit,
        output_retries=5,
    )

    return agent