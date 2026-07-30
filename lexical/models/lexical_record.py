from __future__ import annotations

"""
SanskritAI
==========

Lexical Record

Defines the abstract base class for records originating from
a lexical source.

A LexicalRecord represents one published record within a
LexicalSource. DictionaryEntry is the first concrete
implementation.

Future subclasses
-----------------

DictionaryEntry

CorpusEntry

DhatuEntry

GrammarEntry

AIGeneratedEntry

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.lexical.models.base_lexical_node import (
    BaseLexicalNode,
)
from SanskritAI.lexical.models.base_lexical_metadata import (
    BaseLexicalMetadata,
)
from SanskritAI.lexical.models.lexical_source import (
    LexicalSource,
)


class LexicalRecord(
    BaseLexicalNode[
        str,
        BaseLexicalMetadata,
    ],
    ABC,
):
    """
    Abstract lexical record.
    """

    def __init__(
        self,
        identifier: str,
        metadata: BaseLexicalMetadata,
        source: LexicalSource,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

        self._source = source

    @property
    def source(
        self,
    ) -> LexicalSource:
        """
        Originating lexical source.
        """
        return self._source

    @property
    def source_name(
        self,
    ) -> str:
        return self.source.name

    @property
    def source_identifier(
        self,
    ) -> str:
        return self.source.identifier
