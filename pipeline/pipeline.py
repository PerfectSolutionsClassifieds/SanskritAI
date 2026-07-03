from __future__ import annotations

from lexicon.dictionary import Dictionary
from models.analysis_result import AnalysisResult
from pipeline.stages import PipelineContext
from services.grammar_service import GrammarService
from services.normalization_service import NormalizationService
from services.tokenizer_service import TokenizerService


class AnalysisPipeline:
    """Configurable analysis orchestrator.

    Keep low-level analyzers in `analysis/`; this class owns execution order.
    """

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

    def run(self, text: str) -> AnalysisResult:
        context = PipelineContext(original_text=text)
        context.normalized_text = self.normalizer.normalize(context.original_text)
        context.tokens = self.tokenizer.tokenize(context.normalized_text)
        context.words = self.grammar.analyze_tokens(context.tokens)
        return AnalysisResult(
            original_text=context.original_text,
            normalized_text=context.normalized_text,
            tokens=context.tokens,
            words=context.words,
        )
