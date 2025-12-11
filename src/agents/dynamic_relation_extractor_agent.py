from pydantic import BaseModel
from src.agents.prompts import DYNAMIC_RELATION_EXTRACTOR_PROMPT
from pydantic_ai import Agent

from typing import List

from ._base import model

def create_dynamic_relation_extractor_agent(
        relation_model: BaseModel,
        mention_strings: List[str]
)->Agent:
    relation_extractor_agent = Agent(
            name="relation_extractor_agent",
            model=model,
            retries=5,
            output_type=List[relation_model],
            system_prompt=DYNAMIC_RELATION_EXTRACTOR_PROMPT.format(mentions=mention_strings),
        )

    return relation_extractor_agent
