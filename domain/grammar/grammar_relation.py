from __future__ import annotations

"""
SanskritAI
==========

Grammar Relation

Defines the canonical foundation for grammatical relations in
SanskritAI.

GrammarRelation specializes GrammarCategory for structural and
semantic links between grammatical units, such as:

- agent–action
- subject–predicate
- modifier–modified
- head–dependent
- cause–effect
- location–located

This class is intentionally abstract so that concrete relation
types can later be modeled as specialized immutable value
objects.

Hierarchy
---------

GrammarCategory
        │
        └── GrammarRelation
                ├── SubjectPredicateRelation
                ├── AgentActionRelation
                ├── ModifierHeadRelation
                └── DependencyRelation

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.grammar.grammar_category import GrammarCategory


class GrammarRelation(
    GrammarCategory,
    ABC,
):
    """
    Abstract foundation for Sanskrit grammatical relations.
    """

    @property
    def grammatical_domain(self) -> str:
        """
        Returns the grammatical domain.

        Always:

            relation
        """
        return "relation"

    @property
    def is_role(self) -> bool:
        return False

    @property
    def is_relation(self) -> bool:
        return True

    @property
    def is_feature(self) -> bool:
        return False

    @property
    def is_rule(self) -> bool:
        return False
