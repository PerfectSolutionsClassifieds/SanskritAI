from __future__ import annotations

"""
SanskritAI
==========

Base Knowledge Parser

Abstract base class for all knowledge parsers.

This class specializes the generic BaseParser for structured
knowledge sources such as Amarakośa, Vācaspatyam,
Śabdakalpadruma and future ontology repositories.

Responsibilities
----------------
- Source normalization
- Knowledge text normalization
- Batch parsing helpers
- Parser metadata

Concrete implementations
------------------------
- AmarakoshaParser
- SabdakalpadrumaParser
- VacaspatyamParser
- PuranaOntologyParser

Pipeline
--------

External Source
        ↓
BaseKnowledgeParser
        ↓
KnowledgeRecord

Version
-------
v0.6.0
"""

from __future__ import annotations

from abc import ABC
from typing import Iterable

from SanskritAI.core.parsers.base_parser import BaseParser
from SanskritAI.core.records.knowledge_record import KnowledgeRecord


class BaseKnowledgeParser(
    BaseParser[str],
    ABC,
):
    """
    Base class for all knowledge parsers.
    """

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    def normalize_text(
        self,
        text: str,
    ) -> str:
        """
        Normalize textual values before parsing.
        """
        return text.strip()

    def normalize_optional(
        self,
        text: str | None,
    ) -> str:
        """
        Normalize an optional textual value.
        """
        return "" if text is None else self.normalize_text(text)

    # ---------------------------------------------------------
    # Batch helpers
    # ---------------------------------------------------------

    def parse_lines(
        self,
        lines: Iterable[str],
    ) -> Iterable[KnowledgeRecord[str]]:
        """
        Parse multiple textual lines into KnowledgeRecord
        instances.
        """
        for line in lines:
            line = self.normalize_text(line)

            if not line:
                continue

            yield self.parse(line)

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def subsystem(self) -> str:
        """
        Returns the parser subsystem name.
        """
        return "knowledge"

    @property
    def knowledge_source(self) -> str:
        """
        Returns the knowledge source handled by the parser.

        Concrete subclasses should override this property.
        """
        return "generic"
