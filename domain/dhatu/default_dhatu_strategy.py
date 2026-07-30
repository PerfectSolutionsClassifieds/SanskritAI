from __future__ import annotations

"""
SanskritAI
==========

Default Dhatu Strategy

Canonical rule-based strategy for the Dhatu Kernel.

This implementation mirrors the architecture established by
the Morphology, Grammar and Samāsa kernels.

Pipeline
--------

DhatuContext
      │
      ▼
DhatuRuleSet
      │
      ▼
tuple[Dhatu]
      │
      ▼
DhatuAnalysisCollection
      │
      ▼
DhatuResult

Future
------

Future implementations may replace the simple rule evaluation
with:

    • Dhātupāṭha lookup

    • Paninian derivational engine

    • Multiple repository backends

    • ML ranking

without changing the public API.

Version
-------
v2.0.0
"""

from SanskritAI.domain.dhatu.default_dhatu_rule_set import (
    default_dhatu_rule_set,
)

from SanskritAI.domain.dhatu.dhatu_analysis import (
    DhatuAnalysis,
)

from SanskritAI.domain.dhatu.dhatu_analysis_collection import (
    DhatuAnalysisCollection,
)

from SanskritAI.domain.dhatu.dhatu_context import (
    DhatuContext,
)

from SanskritAI.domain.dhatu.dhatu_diagnostic import (
    DhatuDiagnostic,
)

from SanskritAI.domain.dhatu.dhatu_result import (
    DhatuResult,
)

from SanskritAI.domain.dhatu.dhatu_rule_set import (
    DhatuRuleSet,
)

from SanskritAI.domain.dhatu.dhatu_strategy import (
    DhatuStrategy,
)


class DefaultDhatuStrategy(
    DhatuStrategy,
):
    """
    Canonical rule-based Dhatu strategy.
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

    # ---------------------------------------------------------
    # Rule Set
    # ---------------------------------------------------------

    @property
    def rule_set(self) -> DhatuRuleSet:
        return self._rule_set

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Default Dhatu Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical rule-based Dhatu strategy."
        )

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    def analyze(
        self,
        context: DhatuContext,
    ) -> DhatuResult:
        """
        Performs Dhatu analysis using the configured
        DhatuRuleSet.
        """

        candidates = self.rule_set.apply(
            context
        )

        # ---------------------------------------------
        # No analyses produced
        # ---------------------------------------------

        if not candidates:

            return DhatuResult(

                context=context,

                analyses=DhatuAnalysisCollection(),

                succeeded=False,

                confidence=0.0,

                diagnostics=(

                    DhatuDiagnostic(

                        code="DHATU_NO_ANALYSIS",

                        message=(
                            "No Dhatu analyses were "
                            "produced."
                        ),

                        severity="WARNING",

                        rule=self.display_name,

                    ),

                ),

            )

        # ---------------------------------------------
        # Confidence
        # ---------------------------------------------

        confidence = (
            1.0
            if len(candidates) == 1
            else 0.75
        )

        # ---------------------------------------------
        # Convert Dhatu → DhatuAnalysis
        # ---------------------------------------------

        analyses = DhatuAnalysisCollection()

        for candidate in candidates:

            analyses = analyses.add(

                DhatuAnalysis(

                    dhatu=candidate,

                    confidence=confidence,

                    matched_rule="DhatuRuleSet",

                )

            )

        # ---------------------------------------------
        # Result
        # ---------------------------------------------

        return DhatuResult(

            context=context,

            analyses=analyses,

            succeeded=True,

            confidence=confidence,

            diagnostics=tuple(),

        )
