from __future__ import annotations

"""
SanskritAI
==========

Base Knowledge Record Builder

Abstract adapter responsible for converting immutable
knowledge records into knowledge domain objects.

This class specializes the generic RecordBuilder for the
Knowledge subsystem.

Concrete implementations
------------------------

SynsetRecordBuilder
VargaRecordBuilder

Version
-------
v0.4.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.builders.record_builder import RecordBuilder
from SanskritAI.core.typing import TObject
from SanskritAI.core.records.knowledge_record import KnowledgeRecord


class BaseKnowledgeRecordBuilder(
    RecordBuilder[str, TObject],
    Generic[TObject],
    ABC,
):
    """
    Base class for all knowledge record builders.
    """

    @property
    def record_type(self) -> type[KnowledgeRecord]:
        """
        Returns the primary knowledge record type supported by
        this builder.
        """
        return KnowledgeRecord

    # ---------------------------------------------------------
    # Shared normalization hooks
    # ---------------------------------------------------------

    def normalize_text(
        self,
        text: str,
    ) -> str:
        """
        Normalize textual values.
        """
        return text.strip()

    def normalize_optional(
        self,
        text: str | None,
    ) -> str:
        """
        Normalize optional textual values.
        """
        return "" if text is None else self.normalize_text(text)
