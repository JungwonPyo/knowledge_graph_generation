from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext

from src.models import MyUsage, AgentName
from src.agents._agent_registry import AgentRegistry


@dataclass
class SingleDistillerNode(BaseNode[MyUsage, None, End]):
    raw_document: str

    async def run(
        self,
        ctx: GraphRunContext[MyUsage, None],
    ) -> End:
        result = await AgentRegistry.get(
            AgentName.single_distiller_agent
        ).run(
            user_prompt=self.raw_document,
            model_settings={"temperature": 0, "tool_choice": "auto"},
        )

        usage = result.usage()
        ctx.state.requests += usage.requests
        ctx.state.request_tokens += usage.request_tokens
        ctx.state.response_tokens += usage.response_tokens
        ctx.state.total_tokens += usage.total_tokens

        return End(result.output)
