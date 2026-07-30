from __future__ import annotations

"""
SanskritAI
==========

Default Derivation Strategy

Canonical rule-based strategy for the Morphological Derivation
Kernel.

This version wires in the DerivationPatternRanker so the
canonical repository meaningfully influences output selection
and blueprint preference.

Version
-------
v1.4.0
"""

from SanskritAI.domain.derivation.default_derivation_repository import (
    DefaultDerivationRepository,
)
from SanskritAI.domain.derivation.default_derivation_rule_set import (
    default_derivation_rule_set,
)
from SanskritAI.domain.derivation.derivation_context import (
    DerivationContext,
)
from SanskritAI.domain.derivation.derivation_diagnostic import (
    DerivationDiagnostic,
)
from SanskritAI.domain.derivation.derivation_output import (
    DerivationOutput,
)
from SanskritAI.domain.derivation.derivation_output_collection import (
    DerivationOutputCollection,
)
from SanskritAI.domain.derivation.derivation_pattern_collection import (
    DerivationPatternCollection,
)
from SanskritAI.domain.derivation.derivation_pattern_ranker import (
    DerivationPatternRanker,
)
from SanskritAI.domain.derivation.derivation_repository import (
    DerivationRepository,
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
        repository: DerivationRepository | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_derivation_rule_set()
        )
        self._repository = (
            repository
            if repository is not None
            else DefaultDerivationRepository()
        )
        self._ranker = DerivationPatternRanker(
            repository=self._repository
        )

    # ---------------------------------------------------------
    # Rule Set / Repository / Ranker
    # ---------------------------------------------------------

    @property
    def rule_set(self) -> DerivationRuleSet:
        return self._rule_set

    @property
    def repository(self) -> DerivationRepository:
        return self._repository

    @property
    def ranker(self) -> DerivationPatternRanker:
        return self._ranker

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Default Derivation Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical rule-based derivation strategy."

    # ---------------------------------------------------------
    # Pattern helpers
    # ---------------------------------------------------------

    def _template_patterns(
        self,
        query: str,
    ) -> DerivationPatternCollection:
        """
        Retrieves candidate derivation patterns from the
        configured repository, falling back to the full
        collection if the search is empty.
        """
        patterns = self.repository.search(query)

        if patterns.is_empty:
            return self.repository.all()

        return patterns

    def _best_pattern_name(
        self,
        query: str,
    ) -> str:
        patterns = self._template_patterns(query)

        best = patterns.first
        if best is None:
            return "Derivation Pattern"

        return best.name

    def _build_outputs(
        self,
        context: DerivationContext,
        candidates: tuple[object, ...],
        source_pattern_name: str,
    ) -> DerivationOutputCollection:
        """
        Converts rule outputs into a DerivationOutputCollection.
        """
        outputs = DerivationOutputCollection()

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

            if not surface:
                surface = str(payload.get("value", "")).strip()

            confidence = float(
                payload.get(
                    "confidence",
                    1.0,
                )
            )

            matched_rule = str(
                payload.get(
                    "type",
                    "RuleSet",
                )
            ).strip()

            notes = str(
                payload.get(
                    "analysis",
                    "",
                )
            ).strip()

            pada = str(
                payload.get(
                    "pada",
                    surface,
                )
            ).strip()

            outputs = outputs.add(
                DerivationOutput(
                    identifier=(
                        f"{context.identifier}"
                        f":output:{index}"
                    ),
                    dhatu=context.dhatu,
                    pratyaya=context.pratyaya,
                    surface_form=surface,
                    pada=pada,
                    confidence=confidence,
                    source_pattern=source_pattern_name,
                    matched_rule=matched_rule,
                    notes=notes,
                )
            )

        return outputs

    def _rank_best_pattern_name(
        self,
        outputs: DerivationOutputCollection,
        fallback: str,
    ) -> str:
        """
        Uses the DerivationPatternRanker to find the best
        matching blueprint for the generated outputs.
        """
        ranked = self.ranker.rank(outputs)
        best = ranked.first

        if best is None:
            return fallback

        return best.pattern.name

    def _relabel_outputs(
        self,
        outputs: DerivationOutputCollection,
        pattern_name: str,
    ) -> DerivationOutputCollection:
        """
        Rebuilds outputs with a pattern label chosen by the
        ranker.
        """
        relabeled = DerivationOutputCollection()

        for output in outputs:
            relabeled = relabeled.add(
                DerivationOutput(
                    identifier=output.identifier,
                    dhatu=output.dhatu,
                    pratyaya=output.pratyaya,
                    surface_form=output.surface_form,
                    pada=output.pada,
                    confidence=output.confidence,
                    source_pattern=pattern_name,
                    matched_rule=(
                        f"{pattern_name} :: {output.matched_rule}"
                    ).strip(" :"),
                    notes=output.notes,
                )
            )

        return relabeled

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    def analyze(
        self,
        context: DerivationContext,
    ) -> DerivationResult:
        """
        Performs derivation analysis using the configured
        rule set and the canonical derivation repository.
        """

        candidates = self.rule_set.apply(
            context
        )

        query = (
            f"{context.dhatu.root} "
            f"{context.pratyaya.pratyaya} "
            f"{context.dhatu.meaning} "
            f"{context.pratyaya.meaning}"
        )

        fallback_pattern_name = self._best_pattern_name(query)

        provisional_outputs = self._build_outputs(
            context=context,
            candidates=candidates,
            source_pattern_name=fallback_pattern_name,
        )

        ranked_pattern_name = self._rank_best_pattern_name(
            provisional_outputs,
            fallback=fallback_pattern_name,
        )

        outputs = self._relabel_outputs(
            provisional_outputs,
            pattern_name=ranked_pattern_name,
        )

        if outputs.is_empty:
            return DerivationResult(
                context=context,
                outputs=DerivationOutputCollection(),
                succeeded=False,
                confidence=0.0,
                diagnostics=(
                    DerivationDiagnostic(
                        code="DERIVATION_NO_ANALYSIS",
                        message=(
                            "No derivational outputs were produced."
                        ),
                        severity="WARNING",
                        rule=self.display_name,
                    ),
                ),
            )

        confidence = (
            1.0
            if outputs.count == 1
            else 0.75
        )

        return DerivationResult(
            context=context,
            outputs=outputs,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(),
        )
