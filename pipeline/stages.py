from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class PipelineContext:
    original_text: str
    normalized_text: str = ""
    tokens: list[str] | None = None
    words: list | None = None


class PipelineStage(Protocol):
    name: str

    def run(self, context: PipelineContext) -> PipelineContext:
        ...
