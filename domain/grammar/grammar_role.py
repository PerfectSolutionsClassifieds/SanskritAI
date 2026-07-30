from __future__ import annotations

"""
SanskritAI
==========

Grammar Role

Defines the canonical foundation for Sanskrit grammatical roles
and kāraka-oriented functions.

GrammarRole specializes GrammarCategory for semantic-syntactic
roles such as:

- कर्ता (agent / doer)
- कर्म (object / patient)
- करण (instrument)
- संप्रदान (recipient / beneficiary)
- अपादान (source / separation)
- अधिकरण (locus / location)

This class is intentionally abstract so that concrete roles
can later be modeled as specialized immutable value objects.

Hierarchy
---------

GrammarCategory
        │
        └── GrammarRole
                ├── Kartā
                ├── Karma
                ├── Karaṇa
                ├── Sampradāna
                ├── Apādāna
                └── Adhikaraṇa

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.grammar.grammar_category import GrammarCategory


class GrammarRole(
    GrammarCategory,
    ABC,
):
    """
    Abstract foundation for Sanskrit grammatical roles.
    """

    @property
    def grammatical_domain(self) -> str:
        """
        Returns the grammatical domain.

        Always:

            role
        """
        return "role"

    @property
    def is_role(self) -> bool:
        return True

    @property
    def is_relation(self) -> bool:
        return False

    @property
    def is_feature(self) -> bool:
        return False

    @property
    def is_rule(self) -> bool:
        return False
