from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Parser Contract
--------------------------------

The parser converts acquired source representation into
MonierWilliamsRecord objects.

The parser is deliberately independent of:

* CanonicalKnowledgeRepository
* LexicalRepository
* DictionaryEntry
* DictionarySense
* lexical validation
* linguistic reasoning

This preserves the architectural boundary:

    Source
      |
      v
    Parser
      |
      v
    MonierWilliamsRecord
      |
      v
    Adapter / Mapper
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


class MonierWilliamsParser(ABC):
    """
    Abstract parser for Monier-Williams source representations.
    """

    SOURCE = "monier-williams"

    @abstractmethod
    def parse(
        self,
        source_text: str,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Parse complete source content.
        """
        raise NotImplementedError

    def parse_lines(
        self,
        lines: Iterable[str],
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Convenience method for parsing an iterable of source lines.
        """
        return self.parse(
            "\n".join(lines),
        )
