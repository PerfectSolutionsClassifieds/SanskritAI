from __future__ import annotations

"""
SanskritAI
==========

Search Operator

Defines the canonical logical operators used to combine search
expressions.

SearchOperator specifies *how* multiple search terms or
subqueries are combined.

Typical usages include:

- Corpus search
- Dictionary search
- Knowledge search
- Grammar search

Architecture
------------

SearchOperator
       │
       ▼
SearchQuery

Version
-------
v0.6.0
"""

from enum import Enum


class SearchOperator(str, Enum):
    """
    Canonical search operators.
    """

    # ---------------------------------------------------------
    # Boolean operators
    # ---------------------------------------------------------

    AND = "and"

    OR = "or"

    NOT = "not"

    XOR = "xor"

    # ---------------------------------------------------------
    # Phrase operator
    # ---------------------------------------------------------

    PHRASE = "phrase"

    # ---------------------------------------------------------
    # Proximity search
    # ---------------------------------------------------------

    NEAR = "near"

    # ---------------------------------------------------------
    # Grouping
    # ---------------------------------------------------------

    GROUP = "group"

    @property
    def is_boolean(self) -> bool:
        """
        Returns True if this is a Boolean operator.
        """
        return self in {
            SearchOperator.AND,
            SearchOperator.OR,
            SearchOperator.NOT,
            SearchOperator.XOR,
        }

    @property
    def is_structural(self) -> bool:
        """
        Returns True if this operator defines search structure.
        """
        return self in {
            SearchOperator.PHRASE,
            SearchOperator.NEAR,
            SearchOperator.GROUP,
        }
