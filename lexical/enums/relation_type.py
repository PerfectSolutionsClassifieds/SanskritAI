from __future__ import annotations

"""
Lexical Relation Types.
"""

from enum import Enum


class RelationType(str, Enum):

    SYNONYM = "synonym"

    ANTONYM = "antonym"

    HYPERNYM = "hypernym"

    HYPONYM = "hyponym"

    HOLONYM = "holonym"

    MERONYM = "meronym"

    DERIVED = "derived"

    INFLECTED = "inflected"

    COMPOUND = "compound"

    RELATED = "related"
