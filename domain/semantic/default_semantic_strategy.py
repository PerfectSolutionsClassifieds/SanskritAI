from __future__ import annotations

"""
SanskritAI
==========

Default Semantic Strategy

Canonical semantic strategy for the Semantic Kernel.

This version converts rule outputs into structured
SemanticAnalysis objects, including frames and relations when
available.

Version
-------
v1.1.0
"""

from SanskritAI.domain.semantic.default_semantic_rule_set import (
    default_semantic_rule_set,
)
from SanskritAI.domain.semantic.semantic_analysis import SemanticAnalysis
from SanskritAI.domain.semantic.semantic_analysis_collection import (
    SemanticAnalysisCollection,
)
from SanskritAI.domain.semantic.semantic_context import SemanticContext
from SanskritAI.domain.semantic.semantic_diagnostic import (
    SemanticDiagnostic,
)
from SanskritAI.domain.semantic.semantic_result import SemanticResult
from SanskritAI.domain.semantic.semantic_rule_set import SemanticRuleSet
from SanskritAI.domain.semantic.semantic_strategy import SemanticStrategy


class DefaultSemanticStrategy(
    SemanticStrategy,
):
    """
    Canonical semantic strategy.
    """

    def __init__(
        self,
        rule_set: SemanticRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_semantic_rule_set()
        )

    @property
    def rule_set(self) -> SemanticRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Semantic Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical semantic strategy."

    def _to_analysis_collection(
        self,
        context: SemanticContext,
        candidates: tuple[object, ...],
    ) -> SemanticAnalysisCollection:
        analyses = SemanticAnalysisCollection()

        for index, candidate in enumerate(candidates, start=1):
            payload = candidate if isinstance(candidate, dict) else {"value": candidate}

            text = str(payload.get("text", str(context.subject))).strip()
            meaning = str(payload.get("meaning", "")).strip()
            semantic_type = str(payload.get("type", "Semantic")).strip()
            confidence = float(payload.get("confidence", 1.0))
            matched_rule = str(payload.get("matched_rule", "")).strip()
            notes = str(payload.get("notes", "")).strip()

            frame = payload.get("frame", None)

            if frame is not None:
                if not meaning:
                    meaning = str(getattr(frame, "display_description", "")).strip()
                if not semantic_type or semantic_type == "Semantic":
                    semantic_type = str(getattr(frame, "display_name", "SemanticFrame"))
                if not notes:
                    notes = str(getattr(frame, "notes", "")).strip() or str(
                        getattr(frame, "summary", "")
                    ).strip()

            analyses = analyses.add(
                SemanticAnalysis(
                    identifier=f"{context.identifier}:analysis:{index}",
                    text=text,
                    meaning=meaning,
                    semantic_type=semantic_type,
                    confidence=confidence,
                    matched_rule=matched_rule,
                    notes=notes,
                )
            )

        return analyses

    def analyze(
        self,
        context: SemanticContext,
    ) -> SemanticResult:
        candidates = self.rule_set.apply(context)
        analyses = self._to_analysis_collection(context, candidates)

        if analyses.is_empty:
            return SemanticResult(
                context=context,
                value=SemanticAnalysisCollection(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    SemanticDiagnostic(
                        code="SEMANTIC_NO_ANALYSIS",
                        message="No semantic analyses were produced.",
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = 1.0 if analyses.count == 1 else 0.75

        return SemanticResult(
            context=context,
            value=analyses,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
