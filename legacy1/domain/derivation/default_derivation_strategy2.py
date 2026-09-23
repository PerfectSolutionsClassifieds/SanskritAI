from __future__ import annotations

"""
SanskritAI
==========

Default Derivation Strategy

Canonical rule-based strategy for the Morphological
Derivation Kernel.

This version mirrors the architecture of the Grammar,
Samasa, Dhatu and Pratyaya kernels by producing a
DerivationAnalysisCollection instead of returning raw
candidate tuples.

Version
-------
v1.1.0
"""

from SanskritAI.domain.derivation.default_derivation_rule_set import (
    default_derivation_rule_set,
)

from SanskritAI.domain.derivation.derivation_analysis import (
    DerivationAnalysis,
)

from SanskritAI.domain.derivation.derivation_analysis_collection import (
    DerivationAnalysisCollection,
)

from SanskritAI.domain.derivation.derivation_context import (
    DerivationContext,
)

from SanskritAI.domain.derivation.derivation_diagnostic import (
    DerivationDiagnostic,
)

from SanskritAI.domain.derivation.derivation_result import (
    DerivationResult,
)

from SanskritAI.domain.derivation.derivation_rule_set import (
    DerivationRuleSet,
)

from SanskritAI.domain.derivation.derivation_strategy import (
    DerivationStrategy,
)


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

    # ---------------------------------------------------------

    @property
    def rule_set(
        self,
    ) -> DerivationRuleSet:

        return self._rule_set

    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Default Derivation Strategy"

    @property
    def display_text(
        self,
    ) -> str:

        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:

        return (
            "Canonical rule-based derivation strategy."
        )

    # ---------------------------------------------------------

    def _to_analysis_collection(
        self,
        context: DerivationContext,
        candidates: tuple[object, ...],
    ) -> DerivationAnalysisCollection:
        """
        Converts rule outputs into an immutable
        DerivationAnalysisCollection.
        """

        analyses = DerivationAnalysisCollection()

        for index, candidate in enumerate(
            candidates,
            start=1,
        ):

            payload = (
                candidate
                if isinstance(candidate, dict)
                else {
                    "surface": str(candidate),
                }
            )

            surface = str(
                payload.get(
                    "surface",
                    "",
                )
            ).strip()

            confidence = float(
                payload.get(
                    "confidence",
                    1.0,
                )
            )

            matched_rule = str(
                payload.get(
                    "type",
                    "",
                )
            ).strip()

            notes = str(
                payload.get(
                    "analysis",
                    "",
                )
            ).strip()

            analyses = analyses.add(

                DerivationAnalysis(

                    identifier=(
                        f"{context.identifier}"
                        f":analysis:{index}"
                    ),

                    dhatu=context.dhatu,

                    pratyaya=context.pratyaya,

                    surface_form=surface,

                    confidence=confidence,

                    matched_rule=matched_rule,

                    notes=notes,

                )

            )

        return analyses

    # ---------------------------------------------------------

    def analyze(
        self,
        context: DerivationContext,
    ) -> DerivationResult:
        """
        Performs derivation analysis using the
        configured rule set.
        """

        candidates = self.rule_set.apply(
            context
        )

        analyses = self._to_analysis_collection(
            context,
            candidates,
        )

        if analyses.is_empty:

            return DerivationResult(

                context=context,

                analyses=(
                    DerivationAnalysisCollection()
                ),

                succeeded=False,

                confidence=0.0,

                diagnostics=(

                    DerivationDiagnostic(

                        code=(
                            "DERIVATION_NO_ANALYSIS"
                        ),

                        message=(
                            "No derivational analyses "
                            "were produced."
                        ),

                        severity="WARNING",

                        rule=self.display_name,

                    ),

                ),

            )

        confidence = (
            1.0
            if analyses.count == 1
            else 0.75
        )

        return DerivationResult(

            context=context,

            analyses=analyses,

            succeeded=True,

            confidence=confidence,

            diagnostics=tuple(),

        )
