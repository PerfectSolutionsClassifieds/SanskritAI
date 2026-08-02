from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Matcher

Canonical abstract rule matcher for the Paninian grammar engine.

Purpose
-------
A PaninianRuleMatcher determines whether a particular
PaninianRule is applicable to the current derivational context.

The matcher is intentionally independent of any specific
grammatical kernel.

It evaluates

    • Rule Conditions
    • Rule.supports()
    • Rule.validate()

and produces a PaninianRuleMatchResult.

Architecture
------------

PaninianRule
      │
      ▼
PaninianRuleMatcher
      │
      ├── evaluates RuleCondition(s)
      ├── evaluates supports()
      ├── evaluates validate()
      │
      ▼
PaninianRuleMatchResult

Concrete subclasses

    DefaultPaninianRuleMatcher

Future

    WeightedRuleMatcher

    ExplainableRuleMatcher

    KnowledgeGraphRuleMatcher

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)
from SanskritAI.domain.panini.paninian_rule_match_result import (
    PaninianRuleMatchResult,
)


@dataclass(frozen=True, slots=True)
class PaninianRuleMatcher(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Canonical abstract Paninian rule matcher.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Rule Matcher"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Evaluates applicability of Paninian rules."
        )

    # ---------------------------------------------------------
    # Matching
    # ---------------------------------------------------------

    @abstractmethod
    def match(
        self,
        rule: PaninianRule,
        context: Any,
    ) -> PaninianRuleMatchResult:
        """
        Evaluates whether the supplied rule matches the
        supplied derivational context.

        Parameters
        ----------
        rule
            Paninian rule under evaluation.

        context
            Current derivation context.

        Returns
        -------
        PaninianRuleMatchResult
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def matches(
        self,
        rule: PaninianRule,
        context: Any,
    ) -> bool:
        """
        Returns True iff the rule matches.
        """
        return self.match(
            rule,
            context,
        ).matched

    def supports(
        self,
        rule: PaninianRule,
        context: Any,
    ) -> bool:
        """
        Alias for matches().
        """
        return self.matches(
            rule,
            context,
        )

    # ---------------------------------------------------------
    # Batch Matching
    # ---------------------------------------------------------

    def match_all(
        self,
        rules: tuple[PaninianRule, ...],
        context: Any,
    ) -> tuple[PaninianRuleMatchResult, ...]:
        """
        Evaluates every supplied rule.

        Returns
        -------
        tuple[PaninianRuleMatchResult, ...]
        """

        return tuple(
            self.match(
                rule,
                context,
            )
            for rule in rules
        )

    def matching_rules(
        self,
        rules: tuple[PaninianRule, ...],
        context: Any,
    ) -> tuple[PaninianRuleMatchResult, ...]:
        """
        Returns only successful matches.
        """

        return tuple(
            result
            for result in self.match_all(
                rules,
                context,
            )
            if result.matched
        )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
