from dataclasses import dataclass


@dataclass
class MyUsage:
    requests: int | None = 0
    request_tokens: int | None = 0
    response_tokens: int | None = 0
    total_tokens: int | None = 0
    # distilled_units: List[DistilledUnit] = Field(default_factory=list)