from __future__ import annotations

from lexicon.dictionary import Dictionary
from models.analysis_result import AnalysisResult
from services.grammar_service import GrammarService
from services.normalization_service import NormalizationService
from services.tokenizer_service import TokenizerService


class AnalysisService:
    def __init__(
        self,
        dictionary: Dictionary | None = None,
        normalizer: NormalizationService | None = None,
        tokenizer: TokenizerService | None = None,
        grammar: GrammarService | None = None,
    ):
        self.normalizer = normalizer or NormalizationService()
        self.tokenizer = tokenizer or TokenizerService()
        self.grammar = grammar or GrammarService(dictionary=dictionary)

    def analyze(self, text: str) -> AnalysisResult:
        normalized = self.normalizer.normalize(text)
        tokens = self.tokenizer.tokenize(normalized)
        words = self.grammar.analyze_tokens(tokens)
        return AnalysisResult(
            original_text=text,
            normalized_text=normalized,
            tokens=tokens,
            words=words,
        )
