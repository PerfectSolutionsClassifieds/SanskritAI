from __future__ import annotations

"""
SanskritAI
==========

Lexical Relation Metadata

Metadata describing a semantic or lexical relationship between
two lexical entities.

A relation may connect Lexemes, DictionaryEntries,
DictionarySenses, or other lexical objects.

Version
-------
v0.3.0
"""

from dataclasses import dataclass

from SanskritAI.lexical.enums.relation_type import RelationType
from SanskritAI.lexical.models.base_lexical_metadata import (
    BaseLexicalMetadata,
)


@dataclass(slots=True)
class LexicalRelationMetadata(BaseLexicalMetadata):
    """
    Metadata describing a lexical relationship.
    """

    relation_type: RelationType = RelationType.RELATED

    source_identifier: str = ""

    target_identifier: str = ""

    directed: bool = True

    weight: float = 1.0

    confidence: float = 1.0

    source_dictionary: str = ""

    notes: str = ""
