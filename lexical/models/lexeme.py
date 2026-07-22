from __future__ import annotations

"""
SanskritAI
==========

Lexeme

Represents a canonical lexical unit (lemma).

A Lexeme models an abstract vocabulary item independent of
its inflected forms, dictionary entries, or textual
occurrences.

Examples
--------

गम्

राम

गज

धर्म

Future relationships
--------------------

Lexeme
    ├── DictionaryEntry
    ├── DictionarySense
    ├── MorphologicalAnalysis
    ├── LexicalRelation
    ├── Token occurrences
    └── AI semantic embeddings

Version
-------
v0.3.0
"""

from SanskritAI.lexical.models.base_lexical_node import (
    BaseLexicalNode,
)
from SanskritAI.lexical.models.lexeme_metadata import (
    LexemeMetadata,
)


class Lexeme(
    BaseLexicalNode[
        str,
        LexemeMetadata,
    ]
):
    """
    Canonical lexical unit.
    """

    def __init__(
        self,
        identifier: str,
        metadata: LexemeMetadata,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Convenience aliases
    # ---------------------------------------------------------

    @property
    def lemma(
        self,
    ) -> str:
        """
        Canonical lemma.
        """

        return self.metadata.lemma

    # ---------------------------------------------------------

    @property
    def transliteration(
        self,
    ) -> str:
        """
        Transliterated lemma.
        """

        return self.metadata.transliteration

    # ---------------------------------------------------------

    @property
    def part_of_speech(
        self,
    ):
        """
        Grammatical category.
        """

        return self.metadata.part_of_speech

    # ---------------------------------------------------------

    @property
    def root(
        self,
    ) -> str:
        """
        Dhātu or lexical root, when known.
        """

        return self.metadata.root

    # ---------------------------------------------------------

    @property
    def frequency(
        self,
    ) -> int:
        """
        Corpus frequency.
        """

        return self.metadata.frequency

    # ---------------------------------------------------------

    @property
    def language(
        self,
    ) -> str:
        """
        Language.
        """

        return self.metadata.language

    # ---------------------------------------------------------

    @property
    def script(
        self,
    ) -> str:
        """
        Script.
        """

        return self.metadata.script

    # ---------------------------------------------------------

    @property
    def status(
        self,
    ):
        """
        Editorial status.
        """

        return self.metadata.status
