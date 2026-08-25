from __future__ import annotations

"""
SanskritAI
==========

Corpus

Root domain object representing a canonical corpus.

Corpus is the root ContainerNode of the canonical corpus
hierarchy:

    Corpus
        Document
            Section
                Verse
                    Paragraph
                        Line
                            Token

Structural responsibilities are delegated to ContainerNode and
NodeCollection. Corpus retains the domain-specific ``documents``
vocabulary as an alias for ``children``.

Version
-------
v0.3.1
"""

from typing import TYPE_CHECKING

from SanskritAI.common.identifiers.corpus_id import CorpusId
from SanskritAI.corpus.models.base_node import BaseNode
from SanskritAI.corpus.models.container_node import ContainerNode
from SanskritAI.corpus.models.corpus_metadata import CorpusMetadata

if TYPE_CHECKING:
    from SanskritAI.corpus.models.document import Document


class Corpus(
    ContainerNode[
        CorpusId,
        CorpusMetadata,
        "Document",
    ],
):
    """
    Root container of the canonical corpus hierarchy.

    Corpus participates in the same structural model as every
    other container node while preserving the domain-specific
    ``documents`` terminology.
    """

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(
        self,
        id: CorpusId,
        metadata: CorpusMetadata | None = None,
    ) -> None:
        """
        Construct a Corpus.

        ``id`` is retained as the public constructor parameter for
        compatibility with the existing Corpus API and tests.

        Internally it becomes the canonical BaseNode identifier.
        """

        super().__init__(
            identifier=id,
            metadata=metadata or CorpusMetadata(),
        )

    # ---------------------------------------------------------
    # Documents
    # ---------------------------------------------------------

    @property
    def documents(self):
        """
        Domain-specific alias for ``children``.

        The returned object is the same NodeCollection instance;
        no second collection is maintained.
        """

        return self.children

    # ---------------------------------------------------------

    def add_document(
        self,
        document: "Document",
    ) -> None:
        """
        Add a document to the corpus.
        """

        self.add_child(document)

    # ---------------------------------------------------------

    def remove_document(
        self,
        document: "Document",
    ) -> None:
        """
        Remove a document from the corpus.
        """

        self.remove_child(document)

    # ---------------------------------------------------------

    def clear_documents(
        self,
    ) -> None:
        """
        Remove all documents from the corpus.
        """

        self.clear_children()

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def document_count(self) -> int:
        """
        Number of documents in the corpus.
        """

        return self.child_count

    # ---------------------------------------------------------

    @property
    def first_document(self) -> "Document | None":
        """
        First document in insertion order.
        """

        return self.first_child

    # ---------------------------------------------------------

    @property
    def last_document(self) -> "Document | None":
        """
        Last document in insertion order.
        """

        return self.last_child

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize the corpus into a dictionary.
        """

        return {
            "id": str(self.id),
            "metadata": self.metadata.to_dict(),
            "documents": [
                document.to_dict()
                for document in self.documents
            ],
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Corpus("
            f"id={self.id}, "
            f"title={self.metadata.title!r}, "
            f"documents={self.document_count})"
        )
