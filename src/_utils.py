from typing import TypeVar
from typing import Sequence, Callable, Awaitable

from pydantic_ai.usage import Usage
from tqdm import tqdm

import anyio

from src.models import MyUsage

T = TypeVar("T")

async def task_group_gather(tasks: Sequence[Callable[[], Awaitable[T]]]):

    results: list[T] = [None] * len(tasks)
    print('len result', len(results))

    async def _run_task(tsk: Callable[[], Awaitable[T]], index: int):
        """Helper function to run a task and store the result in the correct index."""
        results[index] = await tsk()

    async with anyio.create_task_group() as tg:
        for i, task in enumerate(tasks):
            tg.start_soon(_run_task, task, i)

    return results

def update_usage(current_usage: MyUsage, new_usage: Usage):

    current_usage.requests += new_usage.requests
    current_usage.request_tokens += new_usage.request_tokens
    current_usage.response_tokens += new_usage.response_tokens
    current_usage.total_tokens += new_usage.total_tokens

    return current_usage
