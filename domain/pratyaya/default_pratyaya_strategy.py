from __future__ import annotations

"""
SanskritAI
==========

Default Pratyaya Strategy

Canonical rule-based strategy for the Pratyaya Kernel.

This refactor optionally consults a canonical
PratyayaCollection or PratyayaRepository so the kernel can
mirror Dhatu more closely while remaining lightweight.

Version
-------
v2.2.0
"""

from SanskritAI.domain.pratyaya.default_pratyaya_repository import (
    DefaultPratyayaRepository,
)
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
from SanskritAI.domain.pratyaya.pratyaya_factory import (
    Pratyaya,
    PratyayaCollection,
    PratyayaFactory,
)
from SanskritAI.domain.pratyaya.pratyaya_repository import (
    PratyayaRepository,
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
        repository: PratyayaRepository | None = None,
        collection: PratyayaCollection | None = None,
    ) -> None:
        self._rule_set = (
            rule_set
            if rule_set is not None
            else default_pratyaya_rule_set()
        )
        self._repository = (
            repository
            if repository is not None
            else DefaultPratyayaRepository()
        )
        self._collection = collection

    @property
    def rule_set(self) -> PratyayaRuleSet:
        return self._rule_set

    @property
    def repository(self) -> PratyayaRepository:
        return self._repository

    @property
    def collection(self) -> PratyayaCollection | None:
        return self._collection

    @property
    def display_name(self) -> str:
        return "Default Pratyaya Strategy"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical rule-based Pratyaya strategy."

    def _canonical_collection(self) -> PratyayaCollection:
        """
        Returns the configured collection or the canonical
        repository-backed collection.
        """
        if self.collection is not None:
            return self.collection

        return self.repository.all()

    def _match_pratyaya(
        self,
        surface: str,
        canonical: PratyayaCollection | None,
    ) -> Pratyaya | None:
        if canonical is None:
            return None

        for item in canonical:
            if surface.endswith(item.pratyaya) or surface == item.pratyaya:
                return item

        return None

    def _to_analysis_collection(
        self,
        context: PratyayaContext,
        candidates: tuple[object, ...],
    ) -> PratyayaAnalysisCollection:
        analyses = PratyayaAnalysisCollection()
        canonical = self._canonical_collection()

        for index, candidate in enumerate(candidates, start=1):
            payload = (
                candidate
                if isinstance(candidate, dict)
                else {"value": candidate}
            )

            pratyaya = str(payload.get("pratyaya", "")).strip()
            transliteration = str(payload.get("transliteration", "")).strip()
            meaning = str(payload.get("meaning", "")).strip()
            confidence = float(payload.get("confidence", 1.0))
            matched_rule = str(payload.get("matched_rule", "RuleSet")).strip()
            notes = str(payload.get("notes", "")).strip()
            category = str(payload.get("category", "")).strip()

            surface = str(context.subject).strip()
            canonical_item = self._match_pratyaya(surface, canonical)

            if canonical_item is not None:
                pratyaya = canonical_item.pratyaya
                transliteration = canonical_item.transliteration
                meaning = canonical_item.meaning or meaning
                category = canonical_item.category or category
                notes = canonical_item.notes or notes

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
                        message="No Pratyaya analyses were produced.",
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
