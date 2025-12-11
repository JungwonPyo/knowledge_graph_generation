from pydantic_ai import Agent
from typing import Callable

from src.models import AgentName

class AgentRegistry:
    _agents: dict[AgentName, Agent] = {}

    @classmethod
    def register(cls, agent_name: AgentName):
        """A decorator to automatically register agent"""

        def decorator(func: Callable) -> Callable:
            cls._agents[agent_name] = func()
            print("Registered agent", agent_name)
            return func
        return decorator

    @classmethod
    def get(cls, agent_name: AgentName) -> Agent:
        return cls._agents[agent_name]