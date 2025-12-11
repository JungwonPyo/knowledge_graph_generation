from ._agent_registry import AgentRegistry
from src.models import AgentName, DistilledUnit
from src.agents.prompts import SINGLE_DISTILLER_AGENT
from pydantic_ai import Agent

from ._base import model

@AgentRegistry.register(AgentName.single_distiller_agent)
def create_single_distiller_agent() -> Agent:
    agent = Agent(
        name=AgentName.single_distiller_agent.value,
        model=model,
        system_prompt=SINGLE_DISTILLER_AGENT,
        output_type=DistilledUnit,
        output_retries=5, 
    )

    return agent