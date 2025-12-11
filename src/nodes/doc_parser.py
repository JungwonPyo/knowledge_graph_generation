from dataclasses import dataclass
from typing import Any, List

from pydantic_graph import BaseNode, GraphRunContext, End

from src.models import MyUsage, AgentName, Unit, DistilledUnit
from src.agents import AgentRegistry
from src.nodes.section_distiller import SectionDistillerNode
from src._utils import update_usage, task_group_gather


@dataclass
class DocParserNode(BaseNode[MyUsage, None, DistilledUnit]):
    raw_document: str

    async def run(
        self,
        ctx: GraphRunContext[MyUsage, None],
    ) -> End[DistilledUnit]:
        # 1) parse document into Unit
        result = await AgentRegistry.get(
            AgentName.doc_parser_agent
        ).run(self.raw_document, model_settings={"temperature": 0})
        usage = result.usage()
        ctx.state = update_usage(ctx.state, usage)

        unit: Unit = result.output
        sections = unit.sections  # list[SectionContent]

        # 2) distill each section in parallel
        section_results = await task_group_gather(
            [
                # each call returns an End[Section], so section_result.data is a Section
                lambda section=section: SectionDistillerNode(section=section).run(ctx)
                for section in sections
            ]
        )

        # 3) build DistilledUnit from per-section results
        distilled_unit = DistilledUnit(
            title=unit.title,
            summary=unit.summary,
            sections=[section_result.data for section_result in section_results],
        )

        return End(distilled_unit)
