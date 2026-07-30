from __future__ import annotations

"""
SanskritAI
==========

Default Alankara Strategy

Canonical Alankara strategy for the Alankara Kernel.

Version
-------
v1.0.0
"""

from SanskritAI.domain.alankara.alankara_analysis import AlankaraAnalysis
from SanskritAI.domain.alankara.alankara_analysis_collection import (
    AlankaraAnalysisCollection,
)
from SanskritAI.domain.alankara.alankara_context import AlankaraContext
from SanskritAI.domain.alankara.alankara_diagnostic import AlankaraDiagnostic
from SanskritAI.domain.alankara.alankara_result import AlankaraResult
from SanskritAI.domain.alankara.alankara_rule_set import AlankaraRuleSet
from SanskritAI.domain.alankara.default_alankara_rule_set import (
    default_alankara_rule_set,
)
from SanskritAI.domain.alankara.alankara_strategy import AlankaraStrategy


class DefaultAlankaraStrategy(
    AlankaraStrategy,
):
    """
    Canonical Alankara strategy.
    """

    def __init__(
        self,
        rule_set: AlankaraRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_alankara_rule_set()
        )

    @property
    def rule_set(self) -> AlankaraRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Alankara Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical Alankara strategy."

    def _to_analysis_collection(
        self,
        context: AlankaraContext,
        candidates: tuple[object, ...],
    ) -> AlankaraAnalysisCollection:
        analyses = AlankaraAnalysisCollection()

        for index, candidate in enumerate(candidates, start=1):
            payload = candidate if isinstance(candidate, dict) else {"value": candidate}

            text = str(payload.get("text", str(context.subject))).strip()
            alankara = str(payload.get("alankara", "")).strip()
            alankara_class = str(payload.get("alankara_class", "")).strip()
            confidence = float(payload.get("confidence", 1.0))
            matched_rule = str(payload.get("matched_rule", "")).strip()
            notes = str(payload.get("notes", "")).strip()

            analyses = analyses.add(
                AlankaraAnalysis(
                    identifier=f"{context.identifier}:analysis:{index}",
                    text=text,
                    alankara=alankara,
                    alankara_class=alankara_class,
                    confidence=confidence,
                    matched_rule=matched_rule,
                    notes=notes,
                )
            )

        return analyses

    def analyze(
        self,
        context: AlankaraContext,
    ) -> AlankaraResult:
        candidates = self.rule_set.apply(context)
        analyses = self._to_analysis_collection(context, candidates)

        if analyses.is_empty:
            return AlankaraResult(
                context=context,
                analyses=AlankaraAnalysisCollection(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    AlankaraDiagnostic(
                        code="ALANKARA_NO_ANALYSIS",
                        message="No Alankara analyses were produced.",
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = 1.0 if analyses.count == 1 else 0.75

        return AlankaraResult(
            context=context,
            analyses=analyses,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
