from __future__ import annotations

"""
SanskritAI
==========

Default Samasa Strategy

Canonical Samasa strategy built on top of a SamasaRuleSet.

This implementation delegates Samasa analysis to the canonical
rule bundle and returns a SamasaResult.

Version
-------
v1.1.0
"""

from SanskritAI.domain.samasa.default_samasa_rule_set import (
    default_samasa_rule_set,
)
from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_diagnostic import SamasaDiagnostic
from SanskritAI.domain.samasa.samasa_result import SamasaResult
from SanskritAI.domain.samasa.samasa_rule_set import SamasaRuleSet
from SanskritAI.domain.samasa.samasa_strategy import SamasaStrategy


class DefaultSamasaStrategy(
    SamasaStrategy,
):
    """
    Default rule-based Samasa strategy.
    """

    def __init__(
        self,
        rule_set: SamasaRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_samasa_rule_set()
        )

    @property
    def rule_set(self) -> SamasaRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Samasa Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Rule-based Samasa strategy using the canonical "
            "Samasa rule set."
        )

    def analyze(
        self,
        context: SamasaContext,
    ) -> SamasaResult:
        """
        Analyzes the supplied Samasa context using the
        configured rule set.
        """
        candidates = self.rule_set.apply(context)

        if not candidates:
            return SamasaResult(
                context=context,
                value=tuple(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    SamasaDiagnostic(
                        code="SAMASA_NO_CANDIDATES",
                        message=(
                            "No Samasa candidates were produced by the "
                            "current rule set."
                        ),
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = 1.0 if len(candidates) == 1 else 0.75

        return SamasaResult(
            context=context,
            value=candidates,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
