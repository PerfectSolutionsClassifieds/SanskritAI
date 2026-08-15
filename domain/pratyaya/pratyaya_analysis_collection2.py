
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional

from SanskritAI.domain.pratyaya.pratyaya_analysis import PratyayaAnalysis


@dataclass(frozen=True)
class PratyayaAnalysisCollection:
    """
    Immutable collection of PratyayaAnalysis objects.

    The collection provides value-oriented access to a sequence of
    Pratyaya analyses while preserving immutability.

    Compatibility:
        ``has_analyses`` is the positive semantic counterpart of
        ``is_empty`` and is used by the orchestration/strategy layer.
    """

    analyses: tuple[PratyayaAnalysis, ...] = ()

    @property
    def count(self) -> int:
        """Return the number of analyses in the collection."""
        return len(self.analyses)

    @property
    def is_empty(self) -> bool:
        """Return True when the collection contains no analyses."""
        return self.count == 0

    @property
    def has_analyses(self) -> bool:
        """
        Return True when the collection contains at least one analysis.

        This is the positive semantic counterpart of ``is_empty`` and
        provides the compatibility API expected by Pratyaya strategies
        and higher-level orchestration code.
        """
        return not self.is_empty

    @property
    def first(self) -> Optional[PratyayaAnalysis]:
        """Return the first analysis, or None when the collection is empty."""
        if self.is_empty:
            return None
        return self.analyses[0]

    @property
    def best(self) -> Optional[PratyayaAnalysis]:
        """
        Return the highest-confidence analysis.

        When multiple analyses have equal confidence, the first
        occurrence is retained.
        """
        if self.is_empty:
            return None

        return max(
            self.analyses,
            key=lambda analysis: analysis.confidence,
        )

    def add(
        self,
        analysis: PratyayaAnalysis,
    ) -> PratyayaAnalysisCollection:
        """
        Return a new collection containing the supplied analysis.

        The current collection is never mutated.
        """
        return PratyayaAnalysisCollection(
            analyses=self.analyses + (analysis,),
        )

    def extend(
        self,
        other: PratyayaAnalysisCollection,
    ) -> PratyayaAnalysisCollection:
        """
        Return a new collection containing both collections.

        The current and supplied collections remain unchanged.
        """
        return PratyayaAnalysisCollection(
            analyses=self.analyses + other.analyses,
        )

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[PratyayaAnalysis]:
        return iter(self.analyses)

    def __getitem__(self, index: int) -> PratyayaAnalysis:
        return self.analyses[index]
