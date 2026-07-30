from __future__ import annotations

"""
SanskritAI
==========

Default Pratyaya Strategy

Canonical rule-based strategy for the Pratyaya Kernel.

This implementation now converts rule outputs into typed
PratyayaAnalysis objects and returns a PratyayaResult.

Version
-------
v2.0.0
"""

from SanskritAI.domain.pratyaya.default_pratyaya_rule_set import (
    default_pratyaya_rule_set,
)
from SanskritAI.domain.pratyaya.pratyaya_analysis import (
    PratyayaAnalysis,
)
from SanskritAI.domain.pratyaya.pratyaya_analysis_collection import (
    PratyayaAnalysisCollection,
)
from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext
from SanskritAI.domain.pratyaya.pratyaya_diagnostic import (
    PratyayaDiagnostic,
)
from SanskritAI.domain.pratyaya.pratyaya_result import PratyayaResult
from SanskritAI.domain.pratyaya.pratyaya_rule_set import PratyayaRuleSet
from SanskritAI.domain.pratyaya.pratyaya_strategy import PratyayaStrategy


class DefaultPratyayaStrategy(
    PratyayaStrategy,
):
    """
    Canonical rule-based Pratyaya strategy.
    """

    def __init__(
        self,
        rule_set: PratyayaRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_pratyaya_rule_set()
        )

    @property
    def rule_set(self) -> PratyayaRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Pratyaya Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical rule-based Pratyaya strategy."

    def _to_analysis_collection(
        self,
        context: PratyayaContext,
        candidates: tuple[object, ...],
    ) -> PratyayaAnalysisCollection:
        analyses = PratyayaAnalysisCollection()

        for index, candidate in enumerate(candidates, start=1):
            payload = candidate if isinstance(candidate, dict) else {"value": candidate}

            pratyaya = str(payload.get("pratyaya", "")).strip()
            transliteration = str(payload.get("transliteration", "")).strip()
            meaning = str(payload.get("meaning", "")).strip()
            confidence = float(payload.get("confidence", 1.0))
            matched_rule = str(payload.get("matched_rule", "RuleSet")).strip()
            notes = str(payload.get("notes", "")).strip()

            if not pratyaya:
                pratyaya = str(payload.get("type", f"candidate-{index}")).strip()

            analyses = analyses.add(
                PratyayaAnalysis(
                    identifier=f"{context.identifier}:analysis:{index}",
                    pratyaya=pratyaya,
                    transliteration=transliteration,
                    meaning=meaning,
                    confidence=confidence,
                    matched_rule=matched_rule,
                    notes=notes,
                )
            )

        return analyses

    def analyze(
        self,
        context: PratyayaContext,
    ) -> PratyayaResult:
        """
        Performs Pratyaya analysis using the configured rule set.
        """
        candidates = self.rule_set.apply(context)
        analyses = self._to_analysis_collection(context, candidates)

        if not analyses.has_analyses:
            return PratyayaResult(
                context=context,
                analyses=PratyayaAnalysisCollection(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    PratyayaDiagnostic(
                        code="PRATYAYA_NO_ANALYSIS",
                        message=(
                            "No Pratyaya analyses were produced."
                        ),
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = 1.0 if analyses.count == 1 else 0.75

        return PratyayaResult(
            context=context,
            analyses=analyses,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
