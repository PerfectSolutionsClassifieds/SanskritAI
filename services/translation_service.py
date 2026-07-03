from __future__ import annotations

from ai.translator import translate_literal
from models.analysis_result import AnalysisResult


class TranslationService:
    def translate(self, result: AnalysisResult) -> str:
        known = [word.meaning for word in result.words if word.meaning]
        return "; ".join(known) if known else translate_literal(result.tokens)
