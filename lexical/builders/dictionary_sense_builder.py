from __future__ import annotations

"""
SanskritAI
==========

Dictionary Sense Builder

Version
-------
v0.3.0
"""

from SanskritAI.lexical.builders.base_lexical_builder import (
    BaseLexicalBuilder,
)
from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)
from SanskritAI.lexical.models.dictionary_sense_metadata import (
    DictionarySenseMetadata,
)


class DictionarySenseBuilder(
    BaseLexicalBuilder[DictionarySense],
):
    """
    Fluent builder for DictionarySense.
    """

    def __init__(self) -> None:
        super().__init__()

        self._identifier = ""
        self._metadata = DictionarySenseMetadata()

    # ---------------------------------------------------------

    def with_identifier(
        self,
        identifier: str,
    ) -> "DictionarySenseBuilder":

        self._identifier = identifier
        return self

    # ---------------------------------------------------------

    def with_sense_number(
        self,
        number: int,
    ) -> "DictionarySenseBuilder":

        self._metadata.sense_number = number
        return self

    # ---------------------------------------------------------

    def with_definition(
        self,
        definition: str,
    ) -> "DictionarySenseBuilder":

        self._metadata.definition = definition
        return self

    # ---------------------------------------------------------

    def with_gloss(
        self,
        gloss: str,
    ) -> "DictionarySenseBuilder":

        self._metadata.gloss = gloss
        return self

    # ---------------------------------------------------------

    def with_semantic_domain(
        self,
        domain: str,
    ) -> "DictionarySenseBuilder":

        self._metadata.semantic_domain = domain
        return self

    # ---------------------------------------------------------

    def build(self) -> DictionarySense:

        return DictionarySense(
            identifier=self._identifier,
            metadata=self._metadata,
        )
