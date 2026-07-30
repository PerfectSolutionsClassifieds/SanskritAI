from __future__ import annotations

"""
SanskritAI
==========

Morphological Rule Set

Defines the immutable ordered collection of
MorphologicalRule objects.

A MorphologicalRuleSet is used by rule-based analyzers to
evaluate a WordForm against a sequence of grammatical rules.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.lexical.word_form import WordForm
from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)
from SanskritAI.domain.morphology.morphological_rule import MorphologicalRule


@dataclass(frozen=True, slots=True)
class MorphologicalRuleSet(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of morphological rules.
    """

    rules: tuple[MorphologicalRule, ...] = field(
        default_factory=tuple,
    )

    @property
    def display_name(self) -> str:
        return "Morphological Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Rules"

    @property
    def display_description(self) -> str:
        return "Immutable ordered collection of morphological rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(
        self,
        rule: MorphologicalRule,
    ) -> "MorphologicalRuleSet":
        """
        Returns a new rule set with the supplied rule appended.
        """
        return MorphologicalRuleSet(
            rules=self.rules + (rule,),
        )

    def apply(
        self,
        word_form: WordForm,
    ) -> MorphologicalAnalysisCollection:
        """
        Applies all matching rules to the supplied word form.
        """
        analyses = MorphologicalAnalysisCollection()

        for rule in self.rules:
            if rule.applies_to(word_form):
                analyses = analyses.extend(rule.apply(word_form))

        return analyses

    def __iter__(self) -> Iterator[MorphologicalRule]:
        return iter(self.rules)

    def __len__(self) -> int:
        return len(self.rules)

    def __getitem__(
        self,
        index: int,
    ) -> MorphologicalRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
