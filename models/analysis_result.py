from __future__ import annotations

from dataclasses import asdict, dataclass, field

from models.base import BaseModel, new_id
from models.word import Word


@dataclass
class AnalysisResult(BaseModel):
    original_text: str
    normalized_text: str
    tokens: list[str]
    words: list[Word]
    id: str = field(default_factory=lambda: new_id("analysis"), kw_only=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "original_text": self.original_text,
            "normalized_text": self.normalized_text,
            "tokens": self.tokens,
            "words": [asdict(word) for word in self.words],
        }
