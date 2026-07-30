from __future__ import annotations

"""
SanskritAI
==========

Default Chandas Strategy

Canonical Chandas strategy for the Chandas Kernel.

Version
-------
v1.0.0
"""

from SanskritAI.domain.chandas.chandas_analysis import ChandasAnalysis
from SanskritAI.domain.chandas.chandas_analysis_collection import (
    ChandasAnalysisCollection,
)
from SanskritAI.domain.chandas.chandas_context import ChandasContext
from SanskritAI.domain.chandas.chandas_diagnostic import ChandasDiagnostic
from SanskritAI.domain.chandas.chandas_result import ChandasResult
from SanskritAI.domain.chandas.chandas_rule_set import ChandasRuleSet
from SanskritAI.domain.chandas.default_chandas_rule_set import (
    default_chandas_rule_set,
)
from SanskritAI.domain.chandas.chandas_strategy import ChandasStrategy


class DefaultChandasStrategy(
    ChandasStrategy,
):
    """
    Canonical Chandas strategy.
    """

    def __init__(
        self,
        rule_set: ChandasRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_chandas_rule_set()
        )

    @property
    def rule_set(self) -> ChandasRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Chandas Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical Chandas strategy."

    def _to_analysis_collection(
        self,
        context: ChandasContext,
        candidates: tuple[object, ...],
    ) -> ChandasAnalysisCollection:
        analyses = ChandasAnalysisCollection()

        for index, candidate in enumerate(candidates, start=1):
            payload = candidate if isinstance(candidate, dict) else {"value": candidate}

            text = str(payload.get("text", str(context.subject))).strip()
            meter = str(payload.get("meter", "")).strip()
            meter_class = str(payload.get("meter_class", "")).strip()
            syllable_count = int(payload.get("syllable_count", 0) or 0)
            pada_count = int(payload.get("pada_count", 0) or 0)
            confidence = float(payload.get("confidence", 1.0))
            matched_rule = str(payload.get("matched_rule", "")).strip()
            notes = str(payload.get("notes", "")).strip()

            analyses = analyses.add(
                ChandasAnalysis(
                    identifier=f"{context.identifier}:analysis:{index}",
                    text=text,
                    meter=meter,
                    meter_class=meter_class,
                    syllable_count=syllable_count,
                    pada_count=pada_count,
                    confidence=confidence,
                    matched_rule=matched_rule,
                    notes=notes,
                )
            )

        return analyses

    def analyze(
        self,
        context: ChandasContext,
    ) -> ChandasResult:
        candidates = self.rule_set.apply(context)
        analyses = self._to_analysis_collection(context, candidates)

        if analyses.is_empty:
            return ChandasResult(
                context=context,
                analyses=ChandasAnalysisCollection(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    ChandasDiagnostic(
                        code="CHANDAS_NO_ANALYSIS",
                        message="No Chandas analyses were produced.",
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = 1.0 if analyses.count == 1 else 0.75

        return ChandasResult(
            context=context,
            analyses=analyses,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
