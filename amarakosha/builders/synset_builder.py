from __future__ import annotations

"""
SanskritAI
==========

Synset Builder

Fluent builder for Amarakośa Synset objects.

Version
-------
v0.4.0
"""

from SanskritAI.amarakosha.builders.base_amarakosha_builder import (
    BaseAmarakoshaBuilder,
)
from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.models.synset_metadata import (
    SynsetMetadata,
)
from SanskritAI.lexical.models.lexeme import Lexeme


class SynsetBuilder(
    BaseAmarakoshaBuilder[Synset],
):
    """
    Fluent builder for Synset.
    """

    def __init__(self) -> None:
        super().__init__()

        self._identifier = ""
        self._metadata = SynsetMetadata()
        self._lexemes: list[Lexeme] = []

    # ---------------------------------------------------------

    def with_identifier(
        self,
        identifier: str,
    ) -> "SynsetBuilder":

        self._identifier = identifier
        return self

    # ---------------------------------------------------------

    def with_metadata(
        self,
        metadata: SynsetMetadata,
    ) -> "SynsetBuilder":

        self._metadata = metadata
        return self

    # ---------------------------------------------------------

    def add_lexeme(
        self,
        lexeme: Lexeme,
    ) -> "SynsetBuilder":

        self._lexemes.append(lexeme)
        return self

    # ---------------------------------------------------------

    def build(self) -> Synset:

        return Synset(
            identifier=self._identifier,
            metadata=self._metadata,
            children=self._lexemes,
        )
