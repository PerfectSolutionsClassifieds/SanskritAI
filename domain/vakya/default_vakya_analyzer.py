from __future__ import annotations

"""
SanskritAI
==========

Default Vakya Analyzer

Light sentence analyzer that consumes outputs from upstream
kernels through context metadata.

Version
-------
v1.0.0
"""

from SanskritAI.domain.vakya.default_vakya_rule_set import (
    default_vakya_rule_set,
)
from SanskritAI.domain.vakya.vakya_analysis import VakyaAnalysis
from SanskritAI.domain.vakya.vakya_analysis_collection import (
    VakyaAnalysisCollection,
)
from SanskritAI.domain.vakya.vakya_context import VakyaContext
from SanskritAI.domain.vakya.vakya_diagnostic import VakyaDiagnostic
from SanskritAI.domain.vakya.vakya_result import VakyaResult
from SanskritAI.domain.vakya.vakya_rule_set import VakyaRuleSet


class DefaultVakyaAnalyzer:
    """
    Thin sentence analyzer over the canonical Vakya rule set.
    """

    def __init__(
        self,
        rule_set: VakyaRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_vakya_rule_set()
        )

    @property
    def rule_set(self) -> VakyaRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Vakya Analyzer"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Light sentence analyzer that folds in upstream "
            "kernel outputs."
        )

    def _to_analysis_collection(
        self,
        context: VakyaContext,
        candidates: tuple[object, ...],
    ) -> VakyaAnalysisCollection:
        analyses = VakyaAnalysisCollection()

        for index, candidate in enumerate(candidates, start=1):
            payload = candidate if isinstance(candidate, dict) else {"value": candidate}

            sentence = str(
                payload.get("sentence", str(context.subject))
            ).strip()

            confidence = float(payload.get("confidence", 1.0))
            analysis_type = str(payload.get("type", "Sentence")).strip()
            matched_rule = str(payload.get("matched_rule", "")).strip()
            notes = str(payload.get("analysis", "")).strip()

            components = payload.get("components", ())
            if not isinstance(components, tuple):
                if isinstance(components, list):
                    components = tuple(components)
                else:
                    components = (components,)

            analyses = analyses.add(
                VakyaAnalysis(
                    identifier=f"{context.identifier}:analysis:{index}",
                    sentence=sentence,
                    components=components,
                    analysis_type=analysis_type,
                    confidence=confidence,
                    matched_rule=matched_rule,
                    notes=notes,
                )
            )

        return analyses

    def analyze(
        self,
        context: VakyaContext,
    ) -> VakyaResult:
        candidates = self.rule_set.apply(context)
        analyses = self._to_analysis_collection(context, candidates)

        if analyses.is_empty:
            return VakyaResult(
                context=context,
                analyses=VakyaAnalysisCollection(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    VakyaDiagnostic(
                        code="VAKYA_NO_ANALYSIS",
                        message=(
                            "No sentence analyses were produced."
                        ),
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = 1.0 if analyses.count == 1 else 0.75

        return VakyaResult(
            context=context,
            analyses=analyses,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
