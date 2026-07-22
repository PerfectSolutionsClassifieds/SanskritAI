from __future__ import annotations

"""
SanskritAI
==========

Dictionary Sense

Represents a single semantic sense within a DictionaryEntry.

A DictionarySense is the smallest semantic unit of the lexical
layer. It encapsulates one editorial meaning assigned by a
particular dictionary.

Hierarchy
---------

Lexeme
    └── DictionaryEntry
            └── DictionarySense

DictionarySense is intentionally a leaf node.

Future semantic layers (ontology, semantic embeddings,
translations, knowledge graphs, etc.) reference
DictionarySense objects without modifying this model.

Version
-------
v0.3.0
"""

from SanskritAI.lexical.models.base_lexical_node import (
    BaseLexicalNode,
)
from SanskritAI.lexical.models.dictionary_sense_metadata import (
    DictionarySenseMetadata,
)


class DictionarySense(
    BaseLexicalNode[
        str,
        DictionarySenseMetadata,
    ]
):
    """
    Represents one editorial meaning of a dictionary entry.
    """

    def __init__(
        self,
        identifier: str,
        metadata: DictionarySenseMetadata,
    ) -> None:
        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Editorial ordering
    # ---------------------------------------------------------

    @property
    def sense_number(self) -> int:
        """
        Ordinal position of the sense within its dictionary entry.
        """
        return self.metadata.sense_number

    # ---------------------------------------------------------
    # Meaning
    # ---------------------------------------------------------

    @property
    def definition(self) -> str:
        """
        Primary definition.
        """
        return self.metadata.definition

    @property
    def short_definition(self) -> str:
        """
        Short definition.
        """
        return self.metadata.short_definition

    @property
    def gloss(self) -> str:
        """
        Gloss or concise meaning.
        """
        return self.metadata.gloss

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @property
    def semantic_domain(self) -> str:
        """
        Semantic domain.
        """
        return self.metadata.semantic_domain

    @property
    def usage_label(self) -> str:
        """
        Usage label.
        """
        return self.metadata.usage_label

    @property
    def register(self) -> str:
        """
        Linguistic register.
        """
        return self.metadata.register

    # ---------------------------------------------------------
    # Linguistic notes
    # ---------------------------------------------------------

    @property
    def grammatical_note(self) -> str:
        """
        Grammatical note.
        """
        return self.metadata.grammatical_note

    @property
    def etymology(self) -> str:
        """
        Etymological note.
        """
        return self.metadata.etymology

    # ---------------------------------------------------------
    # Supporting material
    # ---------------------------------------------------------

    @property
    def examples(self) -> list[str]:
        """
        Usage examples.
        """
        return self.metadata.examples

    @property
    def citations(self) -> list[str]:
        """
        Supporting citations.
        """
        return self.metadata.citations

    @property
    def cross_references(self) -> list[str]:
        """
        Cross references.
        """
        return self.metadata.cross_references
