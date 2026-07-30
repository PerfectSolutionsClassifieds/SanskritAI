from __future__ import annotations

"""
SanskritAI
==========

Derivation Pattern Ranker

Provides a small DerivationOutput-backed ranking layer for the
Morphological Derivation Kernel.

The ranker takes actual derivation outputs and uses them to
rank reusable derivation patterns from the canonical
repository. This makes pattern selection more output-aware and
moves the kernel beyond simple input-query matching.

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from typing import Iterable

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.derivation.derivation_output import (
    DerivationOutput,
)
from SanskritAI.domain.derivation.derivation_output_collection import (
    DerivationOutputCollection,
)
from SanskritAI.domain.derivation.derivation_pattern import (
    DerivationPattern,
)
from SanskritAI.domain.derivation.derivation_pattern_collection import (
    DerivationPatternCollection,
)
from SanskritAI.domain.derivation.derivation_repository import (
    DerivationRepository,
)


@dataclass(frozen=True, slots=True)
class RankedDerivationPattern(
    Displayable,
):
    """
    One derivation pattern together with its computed score.
    """

    pattern: DerivationPattern

    score: float

    reason: str = ""

    @property
    def display_name(self) -> str:
        return self.pattern.display_name

    @property
    def display_text(self) -> str:
        return f"{self.pattern.display_text} [{self.score:.2f}]"

    @property
    def display_description(self) -> str:
        return self.reason or self.pattern.display_description

    def __str__(self) -> str:
        return self.display_text


@dataclass(frozen=True, slots=True)
class RankedDerivationPatternCollection(
    Displayable,
):
    """
    Immutable ordered collection of ranked derivation patterns.
    """

    ranked_patterns: tuple[RankedDerivationPattern, ...]

    @property
    def display_name(self) -> str:
        return "Ranked Derivation Patterns"

    @property
    def display_text(self) -> str:
        return f"{len(self.ranked_patterns)} ranked patterns"

    @property
    def display_description(self) -> str:
        return "Ranked derivation pattern collection."

    @property
    def is_empty(self) -> bool:
        return len(self.ranked_patterns) == 0

    @property
    def count(self) -> int:
        return len(self.ranked_patterns)

    @property
    def first(self) -> RankedDerivationPattern | None:
        if self.is_empty:
            return None
        return self.ranked_patterns[0]

    def __iter__(self):
        return iter(self.ranked_patterns)

    def __len__(self) -> int:
        return len(self.ranked_patterns)

    def __getitem__(self, index: int) -> RankedDerivationPattern:
        return self.ranked_patterns[index]

    def __str__(self) -> str:
        return self.display_text


class DerivationPatternRanker:
    """
    Output-aware derivation pattern ranker.

    The ranker compares actual derivation outputs against the
    canonical repository patterns and assigns a simple score to
    each pattern.
    """

    def __init__(
        self,
        repository: DerivationRepository,
    ) -> None:
        self._repository = repository

    @property
    def repository(self) -> DerivationRepository:
        return self._repository

    @property
    def display_name(self) -> str:
        return "Derivation Pattern Ranker"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Ranks derivation patterns using actual derivation outputs."
        )

    def _normalize_outputs(
        self,
        outputs: DerivationOutputCollection | Iterable[DerivationOutput],
    ) -> tuple[DerivationOutput, ...]:
        if isinstance(outputs, DerivationOutputCollection):
            return outputs.outputs

        return tuple(outputs)

    def _output_query(self, output: DerivationOutput) -> str:
        parts = [
            output.surface_form,
            output.pada,
            output.source_pattern,
            output.matched_rule,
            output.dhatu.root,
            output.dhatu.meaning,
            output.pratyaya.pratyaya,
            output.pratyaya.meaning,
            output.notes,
        ]
        return " ".join(
            part
            for part in parts
            if part
        ).strip()

    def _score_pattern(
        self,
        pattern: DerivationPattern,
        output: DerivationOutput,
    ) -> tuple[float, str]:
        """
        Computes a simple heuristic score for one pattern
        against one derivation output.
        """
        score = 0.0
        reasons: list[str] = []

        query = self._output_query(output).lower()
        template = pattern.template.lower()
        name = pattern.name.lower()
        category = pattern.category.lower()
        description = pattern.description.lower()
        notes = pattern.notes.lower()

        if pattern.identifier and pattern.identifier in query:
            score += 2.0
            reasons.append("identifier match")

        if name and name in query:
            score += 1.5
            reasons.append("name match")

        if template and template in query:
            score += 2.5
            reasons.append("template match")

        if category and category in query:
            score += 0.75
            reasons.append("category match")

        if description and any(token in query for token in description.split()[:6]):
            score += 0.5
            reasons.append("description overlap")

        if notes and any(token in query for token in notes.split()[:6]):
            score += 0.5
            reasons.append("notes overlap")

        if output.source_pattern and output.source_pattern.lower() in name:
            score += 1.0
            reasons.append("source-pattern affinity")

        if output.matched_rule and output.matched_rule.lower() in name:
            score += 0.75
            reasons.append("matched-rule affinity")

        if output.is_confident:
            score += 0.25
            reasons.append("confident output")

        if output.surface_form and output.surface_form in template:
            score += 1.0
            reasons.append("surface/template affinity")

        reason = ", ".join(reasons) if reasons else "default score"
        return score, reason

    def rank(
        self,
        outputs: DerivationOutputCollection | Iterable[DerivationOutput],
    ) -> RankedDerivationPatternCollection:
        """
        Ranks repository patterns using one or more derivation outputs.
        """
        normalized_outputs = self._normalize_outputs(outputs)
        canonical_patterns = self.repository.all()

        if canonical_patterns.is_empty:
            return RankedDerivationPatternCollection(ranked_patterns=tuple())

        scored: list[RankedDerivationPattern] = []

        for pattern in canonical_patterns:
            best_score = 0.0
            best_reason = ""

            for output in normalized_outputs:
                score, reason = self._score_pattern(pattern, output)
                if score > best_score:
                    best_score = score
                    best_reason = reason

            scored.append(
                RankedDerivationPattern(
                    pattern=pattern,
                    score=best_score,
                    reason=best_reason,
                )
            )

        scored.sort(
            key=lambda item: (
                -item.score,
                item.pattern.priority,
                item.pattern.name.lower(),
            )
        )

        return RankedDerivationPatternCollection(
            ranked_patterns=tuple(scored),
        )

    def best(
        self,
        outputs: DerivationOutputCollection | Iterable[DerivationOutput],
    ) -> DerivationPattern | None:
        """
        Returns the top-ranked derivation pattern, if any.
        """
        ranked = self.rank(outputs)
        first = ranked.first
        if first is None:
            return None
        return first.pattern

    def rank_patterns(
        self,
        outputs: DerivationOutputCollection | Iterable[DerivationOutput],
    ) -> DerivationPatternCollection:
        """
        Returns the ranked patterns as a plain PatternCollection,
        ordered by descending score.
        """
        ranked = self.rank(outputs)
        return DerivationPatternCollection(
            patterns=tuple(
                item.pattern
                for item in ranked
            )
        )
