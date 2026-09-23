from __future__ import annotations

"""
SanskritAI
==========

Amarakośa Synset

Represents a traditional Amarakośa synonym group.

Unlike DictionarySense, a Synset is a container of Lexemes.
It models one semantic grouping within the Amarakośa.

Hierarchy
---------

Amarakanda
    └── Varga
            └── Synset
                    ├── Lexeme
                    ├── Lexeme
                    ├── Lexeme
                    └── ...

Version
-------
v0.4.0
"""

from typing import Iterable

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)

from SanskritAI.lexical.models.lexeme import (
    Lexeme,
)

from SanskritAI.amarakosha.models.synset_metadata import (
    SynsetMetadata,
)


class Synset(
    ContainerNode[
        str,
        SynsetMetadata,
        Lexeme,
    ]
):
    """
    Amarakośa synonym group.

    A Synset contains one or more canonical Lexemes that
    together express a shared semantic concept.
    """

    def __init__(
        self,
        identifier: str,
        metadata: SynsetMetadata,
        children: Iterable[Lexeme] | None = None,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
            children=children,
        )

    # ---------------------------------------------------------
    # Convenience aliases
    # ---------------------------------------------------------

    @property
    def lexemes(self):
        """
        Iterate over the lexemes contained in this synset.
        """
        return iter(self.children)

    @property
    def kanda(self):
        """
        Amarakośa kāṇḍa.
        """
        return self.metadata.kanda

    @property
    def varga(self) -> str:
        """
        Amarakośa varga.
        """
        return self.metadata.varga

    @property
    def varga_number(self) -> int:
        """
        Canonical varga number.
        """
        return self.metadata.varga_number

    @property
    def verse_number(self) -> int:
        """
        Verse containing this synset.
        """
        return self.metadata.verse_number

    @property
    def pada_number(self) -> int:
        """
        Pada containing this synset.
        """
        return self.metadata.pada_number

    @property
    def synset_identifier(self) -> str:
        """
        Canonical Amarakośa synset identifier.
        """
        return self.metadata.synset_identifier

    # ---------------------------------------------------------

    def add_lexeme(
        self,
        lexeme: Lexeme,
    ) -> None:
        """
        Add a lexeme to the synonym group.
        """
        self.add_child(lexeme)

    # ---------------------------------------------------------

    def remove_lexeme(
        self,
        lexeme: Lexeme,
    ) -> None:
        """
        Remove a lexeme from the synonym group.
        """
        self.remove_child(lexeme)
