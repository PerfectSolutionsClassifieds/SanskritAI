from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Strategy

Canonical Sandhi strategy built on top of a SandhiRuleSet.

This implementation delegates Sandhi resolution to the
canonical rule bundle and returns a SandhiResult.

Version
-------
v1.0.0
"""

from SanskritAI.domain.sandhi.default_sandhi_rule_set import (
    default_sandhi_rule_set,
)
from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)
from SanskritAI.domain.sandhi.sandhi_diagnostic import (
    SandhiDiagnostic,
)
from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)
from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)
from SanskritAI.domain.sandhi.sandhi_strategy import (
    SandhiStrategy,
)


class DefaultSandhiStrategy(
    SandhiStrategy,
):
    """
    Default rule-based Sandhi strategy.
    """

    def __init__(
        self,
        rule_set: SandhiRuleSet | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_sandhi_rule_set()
        )

    @property
    def rule_set(self) -> SandhiRuleSet:
        return self._rule_set

    @property
    def display_name(self) -> str:
        return "Default Sandhi Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Rule-based Sandhi strategy using the canonical "
            "Sandhi rule set."
        )

    def resolve(
        self,
        context: SandhiContext,
    ) -> SandhiResult:
        """
        Resolves the supplied Sandhi context using the
        configured rule set.
        """
        candidates = self.rule_set.apply(context)

        if not candidates:
            return SandhiResult(
                context=context,
                value=tuple(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    SandhiDiagnostic(
                        code="SANDHI_NO_CANDIDATES",
                        message=(
                            "No Sandhi candidates were produced by the "
                            "current rule set."
                        ),
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = (
            1.0
            if len(candidates) == 1
            else 0.75
        )

        return SandhiResult(
            context=context,
            value=candidates,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
