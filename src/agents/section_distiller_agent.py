from ._agent_registry import AgentRegistry
from src.models import AgentName, Section, SectionContent
from src.agents.prompts import SECTION_DISTILLER_AGENT
from pydantic_ai import Agent

from ._base import model

@AgentRegistry.register(AgentName.section_distiller_agent)
def create_section_distiller_agent() -> Agent:
    agent = Agent(
        name=AgentName.section_distiller_agent.value,
        model=model,
        system_prompt=SECTION_DISTILLER_AGENT,
        output_type=Section,
        # output_type=SectionContent,
        output_retries=5, 
    )

    return agent