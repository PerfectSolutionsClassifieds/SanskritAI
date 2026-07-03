from __future__ import annotations

from dataclasses import dataclass, field

from models.base import BaseModel, new_id
from models.word import Word


@dataclass
class Sloka(BaseModel):
    text: str
    id: str = field(default_factory=lambda: new_id("sloka"), kw_only=True)
    corpus_id: str | None = None
    book_id: str | None = None
    chapter_id: str | None = None
    words: list[Word] = field(default_factory=list)
