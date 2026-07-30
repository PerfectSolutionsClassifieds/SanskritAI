from __future__ import annotations

"""
SanskritAI
==========

Grammar Feature

Defines the canonical foundation for grammatical features in
SanskritAI.

GrammarFeature specializes GrammarCategory for reusable
grammatical descriptors such as:

- syntactic flags
- kāraka-linked labels
- tense-like markers
- semantic grammar annotations
- structural grammatical tags

This class is intentionally abstract so that concrete features
can later be modeled as specialized immutable value objects.

Hierarchy
---------

GrammarCategory
        │
        └── GrammarFeature
                ├── TenseFeature
                ├── AspectFeature
                ├── VoiceFeature
                ├── KārakaFeature
                └── SyntaxFeature

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.grammar.grammar_category import GrammarCategory


class GrammarFeature(
    GrammarCategory,
    ABC,
):
    """
    Abstract foundation for Sanskrit grammatical features.
    """

    @property
    def grammatical_domain(self) -> str:
        """
        Returns the grammatical domain.

        Always:

            feature
        """
        return "feature"

    @property
    def is_role(self) -> bool:
        return False

    @property
    def is_relation(self) -> bool:
        return False

    @property
    def is_feature(self) -> bool:
        return True

    @property
    def is_rule(self) -> bool:
        return False
