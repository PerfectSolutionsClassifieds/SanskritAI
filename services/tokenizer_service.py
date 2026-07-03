from __future__ import annotations

from analysis.tokenizer import tokenize


class TokenizerService:
    def tokenize(self, text: str) -> list[str]:
        return tokenize(text)
