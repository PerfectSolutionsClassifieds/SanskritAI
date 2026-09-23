from __future__ import annotations

"""
SanskritAI
==========

Default Pratyaya Strategy

Canonical rule-based strategy for the Pratyaya Kernel.

This implementation mirrors the architecture established by
the Morphology, Grammar, Samasa, and Dhatu kernels.

Pipeline
--------

PratyayaContext
      │
      ▼
PratyayaRuleSet
      │
      ▼
tuple[object]
      │
      ▼
PratyayaResult

Version
-------
v1.0.0
"""

from SanskritAI.domain.pratyaya.default_pratyaya_rule_set import (
    default_pratyaya_rule_set,
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
        return (
            "Canonical rule-based Pratyaya strategy."
        )

    def analyze(
        self,
        context: PratyayaContext,
    ) -> PratyayaResult:
        """
        Performs Pratyaya analysis using the configured rule set.
        """
        candidates = self.rule_set.apply(context)

        if not candidates:
            return PratyayaResult(
                context=context,
                value=tuple(),
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

        confidence = 1.0 if len(candidates) == 1 else 0.75

        return PratyayaResult(
            context=context,
            value=candidates,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
