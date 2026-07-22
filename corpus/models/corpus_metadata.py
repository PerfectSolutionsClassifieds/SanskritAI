from __future__ import annotations

"""
SanskritAI
==========

Corpus Metadata

Canonical metadata describing an entire corpus.

Version
-------
v0.2.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.common.metadata.provenance import Provenance

from SanskritAI.corpus.models.classification import (
    Classification,
)


@dataclass(slots=True)
class CorpusMetadata:
    """
    Canonical metadata describing a corpus.
    """

    # ---------------------------------------------------------
    # Identification
    # ---------------------------------------------------------

    title: str = ""

    canonical_title: str = ""

    work_identifier: str = ""

    # ---------------------------------------------------------
    # Contributors
    # ---------------------------------------------------------

    authors: list[str] = field(default_factory=list)

    editors: list[str] = field(default_factory=list)

    translators: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Publication
    # ---------------------------------------------------------

    publisher: str = ""

    publication: str = ""

    edition: str = ""

    publication_year: str = ""

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    classification: Classification = field(
        default_factory=Classification
    )

    # ---------------------------------------------------------
    # Rights
    # ---------------------------------------------------------

    license: str = ""

    copyright: str = ""

    # ---------------------------------------------------------
    # Description
    # ---------------------------------------------------------

    description: str = ""

    keywords: list[str] = field(default_factory=list)

    notes: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    provenance: Provenance | None = None

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_classification(self) -> bool:
        return not self.classification.is_unknown

    @property
    def has_provenance(self) -> bool:
        return self.provenance is not None

    # ---------------------------------------------------------

    def add_author(self, author: str) -> None:
        if author and author not in self.authors:
            self.authors.append(author)

    def add_editor(self, editor: str) -> None:
        if editor and editor not in self.editors:
            self.editors.append(editor)

    def add_translator(self, translator: str) -> None:
        if translator and translator not in self.translators:
            self.translators.append(translator)

    def add_keyword(self, keyword: str) -> None:
        keyword = keyword.strip()
        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword)

    def add_note(self, note: str) -> None:
        note = note.strip()
        if note:
            self.notes.append(note)

    # ---------------------------------------------------------
    # Merge
    # ---------------------------------------------------------

    def merge(
        self,
        other: "CorpusMetadata",
    ) -> None:
        """
        Merge another metadata object into this one.
        Empty values are replaced; collections are merged.
        """

        if not self.title:
            self.title = other.title

        if not self.canonical_title:
            self.canonical_title = other.canonical_title

        if not self.work_identifier:
            self.work_identifier = other.work_identifier

        for author in other.authors:
            self.add_author(author)

        for editor in other.editors:
            self.add_editor(editor)

        for translator in other.translators:
            self.add_translator(translator)

        for keyword in other.keywords:
            self.add_keyword(keyword)

        for note in other.notes:
            self.add_note(note)

    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:

        return {

            "title": self.title,

            "canonical_title": self.canonical_title,

            "work_identifier": self.work_identifier,

            "authors": self.authors,

            "editors": self.editors,

            "translators": self.translators,

            "publisher": self.publisher,

            "publication": self.publication,

            "edition": self.edition,

            "publication_year": self.publication_year,

            "classification":
                self.classification.to_dict(),

            "license": self.license,

            "copyright": self.copyright,

            "description": self.description,

            "keywords": self.keywords,

            "notes": self.notes,

            "provenance":
                self.provenance.to_dict()
                if self.provenance
                else None,

        }
