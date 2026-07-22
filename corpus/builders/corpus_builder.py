from __future__ import annotations

"""
SanskritAI
==========

Corpus Builder

Builder for constructing Corpus objects.

Version
-------
v0.1.0
"""

from SanskritAI.common.identifiers.corpus_id import CorpusId

from SanskritAI.corpus.builders.base_builder import (
    BaseBuilder,
)

from SanskritAI.corpus.models.corpus import (
    Corpus,
)

from SanskritAI.corpus.models.corpus_metadata import (
    CorpusMetadata,
)

from SanskritAI.corpus.models.document import (
    Document,
)


class CorpusBuilder(
    BaseBuilder[Corpus]
):
    """
    Builder for Corpus.
    """

    # ---------------------------------------------------------

    def _create_instance(self) -> Corpus:

        return Corpus(
            id=CorpusId.generate(),
            metadata=CorpusMetadata(),
        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def with_metadata(
        self,
        metadata: CorpusMetadata,
    ) -> "CorpusBuilder":

        self._instance.metadata = metadata

        return self

    # ---------------------------------------------------------

    def with_title(
        self,
        title: str,
    ) -> "CorpusBuilder":

        self._instance.metadata.title = title

        return self

    # ---------------------------------------------------------

    def with_description(
        self,
        description: str,
    ) -> "CorpusBuilder":

        self._instance.metadata.description = description

        return self

    # ---------------------------------------------------------
    # Documents
    # ---------------------------------------------------------

    def add_document(
        self,
        document: Document,
    ) -> "CorpusBuilder":

        self._instance.add_document(
            document,
        )

        return self

    # ---------------------------------------------------------

    def add_documents(
        self,
        documents: list[Document],
    ) -> "CorpusBuilder":

        for document in documents:

            self._instance.add_document(
                document,
            )

        return self

    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Validate the corpus.
        """

        if not self._instance.metadata.title.strip():

            raise ValueError(
                "Corpus title cannot be empty."
            )

    # ---------------------------------------------------------

    @classmethod
    def from_corpus(
        cls,
        corpus: Corpus,
    ) -> "CorpusBuilder":

        return cls().from_instance(
            corpus,
        )
