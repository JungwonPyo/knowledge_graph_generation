from dataclasses import dataclass
from typing import Any

from pydantic_graph import BaseNode, GraphRunContext, End

from src.models import MyUsage, AgentName, Section, SectionContent, build_dynamic_relation_model
from src.agents import AgentRegistry, create_dynamic_relation_extractor_agent
from src._utils import update_usage


@dataclass
class SectionDistillerNode(BaseNode[MyUsage, None, Section]):
    section: SectionContent

    async def run(self, ctx: GraphRunContext[MyUsage, None]) -> End[Section]:
        # 1) distill section (summary + mentions)
        distilled_result = await AgentRegistry.get(
            AgentName.section_distiller_agent
        ).run(
            user_prompt=f"section_title:{self.section.title}\nsection_content:{self.section.content}",
            model_settings={"temperature": 0},
        )
        usage = distilled_result.usage()
        ctx.state = update_usage(ctx.state, usage)

        distilled_section: Section = distilled_result.output

        # 2) build dynamic relation model and extractor
        mentions = distilled_section.mentions
        mention_strings = [m.string for m in mentions]

        relation_model = build_dynamic_relation_model(mention_strings=mention_strings)
        relation_extractor_agent = create_dynamic_relation_extractor_agent(
            relation_model=relation_model,
            mention_strings=mention_strings,
        )

        # 3) extract relations
        relation_result = await relation_extractor_agent.run(
            user_prompt=f"section_title:{self.section.title}\nsection_content:{self.section.content}",
            model_settings={"temperature": 0},
        )
        usage = relation_result.usage()
        ctx.state = update_usage(ctx.state, usage)

        distilled_section.relations = relation_result.output

        return End(distilled_section)
    
        # distilled_section.relations = []  # or None
        # return End(distilled_section)
