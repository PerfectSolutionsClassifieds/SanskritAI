from __future__ import annotations

"""
SanskritAI
==========

Base Metadata

Abstract metadata shared by all canonical corpus entities.

Purpose
-------
Provides common metadata fields reused by CorpusMetadata,
DocumentMetadata, SectionMetadata and future metadata models.

Version
-------
v0.1.0
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Any

from SanskritAI.common.metadata.provenance import Provenance

from SanskritAI.corpus.models.classification import (
    Classification,
)


@dataclass(slots=True)
class BaseMetadata(ABC):
    """
    Base metadata class for all corpus entities.
    """

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    classification: Classification = field(
        default_factory=Classification
    )

    # ---------------------------------------------------------
    # Description
    # ---------------------------------------------------------

    description: str = ""

    keywords: list[str] = field(
        default_factory=list
    )

    notes: list[str] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    provenance: Provenance | None = None

    # ---------------------------------------------------------

    @property
    def has_classification(self) -> bool:

        return not self.classification.is_unknown

    # ---------------------------------------------------------

    @property
    def has_provenance(self) -> bool:

        return self.provenance is not None

    # ---------------------------------------------------------

    def add_keyword(
        self,
        keyword: str,
    ) -> None:

        keyword = keyword.strip()

        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword)

    # ---------------------------------------------------------

    def add_note(
        self,
        note: str,
    ) -> None:

        note = note.strip()

        if note:
            self.notes.append(note)

    # ---------------------------------------------------------

    def metadata_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize common metadata fields.
        """

        return {

            "classification":
                self.classification.to_dict(),

            "description":
                self.description,

            "keywords":
                list(self.keywords),

            "notes":
                list(self.notes),

            "provenance":
                (
                    self.provenance.to_dict()
                    if self.provenance
                    else None
                ),

        }
