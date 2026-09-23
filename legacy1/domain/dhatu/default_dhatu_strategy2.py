from __future__ import annotations

"""
SanskritAI
==========

Default Dhatu Strategy

Canonical Dhatu strategy built on top of a DhatuRuleSet.

This implementation delegates root analysis to the canonical
rule bundle and returns a DhatuResult.

Version
-------
v1.1.0
"""

from SanskritAI.domain.dhatu.default_dhatu_rule_set import (
    default_dhatu_rule_set,
)
from SanskritAI.domain.dhatu.dhatu_context import DhatuContext
from SanskritAI.domain.dhatu.dhatu_diagnostic import DhatuDiagnostic
from SanskritAI.domain.dhatu.dhatu_result import DhatuResult
from SanskritAI.domain.dhatu.dhatu_rule_set import DhatuRuleSet
from SanskritAI.domain.dhatu.dhatu_strategy import DhatuStrategy


class DefaultDhatuStrategy(
    DhatuStrategy,
):
    """
    Default rule-based Dhatu strategy.
    """

    def __init__(
        self,
        rule_set: DhatuRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_dhatu_rule_set()
        )

    @property
    def rule_set(self) -> DhatuRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Dhatu Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Rule-based Dhatu strategy using the canonical "
            "Dhatu rule set."
        )

    def analyze(
        self,
        context: DhatuContext,
    ) -> DhatuResult:
        """
        Analyzes the supplied Dhatu context using the
        configured rule set.
        """
        candidates = self.rule_set.apply(context)

        if not candidates:
            return DhatuResult(
                context=context,
                value=tuple(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    DhatuDiagnostic(
                        code="DHATU_NO_CANDIDATES",
                        message=(
                            "No Dhatu candidates were produced by the "
                            "current rule set."
                        ),
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = 1.0 if len(candidates) == 1 else 0.75

        return DhatuResult(
            context=context,
            value=candidates,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
