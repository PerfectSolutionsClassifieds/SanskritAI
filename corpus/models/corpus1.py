from __future__ import annotations

"""
SanskritAI
==========

Corpus

Root domain object representing a canonical corpus.

A Corpus is the top-level container within the SanskritAI
Canonical Corpus Model.

Version
-------
v0.1.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.common.identifiers.corpus_id import CorpusId

from SanskritAI.corpus.models.corpus_metadata import (
    CorpusMetadata,
)

# Imported lazily for typing only.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SanskritAI.corpus.models.document import Document


@dataclass(slots=True)
class Corpus:
    """
    Canonical corpus.
    """

    id: CorpusId

    metadata: CorpusMetadata = field(
        default_factory=CorpusMetadata
    )

    documents: list["Document"] = field(
        default_factory=list
    )

    # ---------------------------------------------------------

    def add_document(
        self,
        document: "Document",
    ) -> None:

        self.documents.append(document)

    # ---------------------------------------------------------

    def remove_document(
        self,
        document: "Document",
    ) -> None:

        self.documents.remove(document)

    # ---------------------------------------------------------

    def clear_documents(
        self,
    ) -> None:

        self.documents.clear()

    # ---------------------------------------------------------

    @property
    def document_count(
        self,
    ) -> int:

        return len(self.documents)

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self.documents)

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator["Document"]:

        return iter(self.documents)

    # ---------------------------------------------------------

    def __getitem__(
        self,
        index: int,
    ) -> "Document":

        return self.documents[index]

    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> dict:

        return {

            "id": str(self.id),

            "metadata":
                self.metadata.to_dict(),

            "documents":
                [

                    document.to_dict()

                    for document in self.documents

                ],

        }

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"Corpus("

            f"id={self.id}, "

            f"title={self.metadata.title!r}, "

            f"documents={len(self.documents)})"

        )
