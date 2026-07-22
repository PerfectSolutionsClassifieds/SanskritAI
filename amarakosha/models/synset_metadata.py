from __future__ import annotations

"""
SanskritAI
==========

Amarakośa Synset Metadata

Metadata describing a canonical synonym group within the
Amarakośa knowledge base.

A Synset represents one semantic grouping of lexemes as
organized by the traditional Amarakośa. While the term
"synset" is used for interoperability with modern lexical
resources (e.g., WordNet), the underlying model preserves
the traditional Amarakośa hierarchy.

Hierarchy
---------

Amarakanda
    └── Varga
            └── Synset
                    └── Lexemes

Version
-------
v0.4.0
"""

from dataclasses import dataclass

from SanskritAI.lexical.models.base_lexical_metadata import (
    BaseLexicalMetadata,
)
from SanskritAI.amarakosha.enums.Amarakanda import (
    Amarakanda,
)


@dataclass(slots=True)
class SynsetMetadata(BaseLexicalMetadata):
    """
    Metadata describing an Amarakośa synonym group.
    """

    # ---------------------------------------------------------
    # Amarakośa hierarchy
    # ---------------------------------------------------------

    kanda: Amarakanda = Amarakanda.SVARGADI

    varga: str = ""

    varga_number: int = 0

    verse_number: int = 0

    pada_number: int = 0

    # ---------------------------------------------------------
    # Synset identity
    # ---------------------------------------------------------

    synset_identifier: str = ""

    title: str = ""

    # ---------------------------------------------------------
    # Editorial information
    # ---------------------------------------------------------

    commentary: str = ""

    source_edition: str = ""

    notes: str = ""

    # ---------------------------------------------------------
    # External mappings
    # ---------------------------------------------------------

    wordnet_id: str = ""

    external_identifier: str = ""
