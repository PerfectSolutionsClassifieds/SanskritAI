from __future__ import annotations

"""
SanskritAI
==========

Default Derivation Strategy

Canonical rule-based strategy for the Morphological Derivation
Kernel.

This implementation mirrors the architecture established by
the Morphology, Grammar, Samasa, Dhatu, and Pratyaya kernels.

Version
-------
v1.0.0
"""

from SanskritAI.domain.derivation.default_derivation_rule_set import (
    default_derivation_rule_set,
)
from SanskritAI.domain.derivation.derivation_context import DerivationContext
from SanskritAI.domain.derivation.derivation_diagnostic import (
    DerivationDiagnostic,
)
from SanskritAI.domain.derivation.derivation_result import DerivationResult
from SanskritAI.domain.derivation.derivation_rule_set import DerivationRuleSet
from SanskritAI.domain.derivation.derivation_strategy import DerivationStrategy


class DefaultDerivationStrategy(
    DerivationStrategy,
):
    """
    Canonical rule-based derivation strategy.
    """

    def __init__(
        self,
        rule_set: DerivationRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_derivation_rule_set()
        )

    @property
    def rule_set(self) -> DerivationRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Derivation Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical rule-based derivation strategy."

    def analyze(
        self,
        context: DerivationContext,
    ) -> DerivationResult:
        """
        Performs derivation analysis using the configured rule set.
        """
        candidates = self.rule_set.apply(context)

        if not candidates:
            return DerivationResult(
                context=context,
                value=tuple(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    DerivationDiagnostic(
                        code="DERIVATION_NO_ANALYSIS",
                        message=(
                            "No derivational candidates were produced."
                        ),
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = 1.0 if len(candidates) == 1 else 0.75

        return DerivationResult(
            context=context,
            value=candidates,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
