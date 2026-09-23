
from __future__ import annotations

from SanskritAI.common.identifiers.corpus_id import CorpusId
from SanskritAI.corpus.models.corpus import Corpus
from SanskritAI.corpus.models.corpus_metadata import CorpusMetadata
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.document_metadata import DocumentMetadata


def make_corpus(identifier="corpus-1"):
    return Corpus(
        id=CorpusId(identifier),
        metadata=CorpusMetadata(),
    )


def make_document(identifier="document-1"):
    return Document(
        identifier=identifier,
        metadata=DocumentMetadata(),
    )


def test_corpus_stores_identifier():
    corpus = make_corpus()

    assert str(corpus.id) == "corpus-1"


def test_corpus_stores_metadata():
    metadata = CorpusMetadata()

    corpus = Corpus(
        id=CorpusId("corpus-1"),
        metadata=metadata,
    )

    assert corpus.metadata is metadata


def test_corpus_starts_without_documents():
    corpus = make_corpus()

    assert corpus.documents == []
    assert corpus.document_count == 0
    assert len(corpus) == 0


def test_add_document():
    corpus = make_corpus()
    document = make_document()

    corpus.add_document(document)

    assert corpus.documents == [document]
    assert corpus.document_count == 1


def test_add_documents_preserves_order():
    corpus = make_corpus()

    first = make_document("document-1")
    second = make_document("document-2")

    corpus.add_document(first)
    corpus.add_document(second)

    assert corpus.documents == [first, second]


def test_remove_document():
    corpus = make_corpus()

    first = make_document("document-1")
    second = make_document("document-2")

    corpus.add_document(first)
    corpus.add_document(second)

    corpus.remove_document(first)

    assert corpus.documents == [second]
    assert corpus.document_count == 1


def test_clear_documents():
    corpus = make_corpus()

    corpus.add_document(make_document("document-1"))
    corpus.add_document(make_document("document-2"))

    corpus.clear_documents()

    assert corpus.documents == []
    assert corpus.document_count == 0


def test_iteration_returns_documents():
    corpus = make_corpus()

    first = make_document("document-1")
    second = make_document("document-2")

    corpus.add_document(first)
    corpus.add_document(second)

    assert list(corpus) == [first, second]


def test_index_access_returns_document():
    corpus = make_corpus()

    document = make_document()
    corpus.add_document(document)

    assert corpus[0] is document


def test_negative_index_access():
    corpus = make_corpus()

    first = make_document("document-1")
    second = make_document("document-2")

    corpus.add_document(first)
    corpus.add_document(second)

    assert corpus[-1] is second


def test_to_dict_contains_identifier():
    corpus = make_corpus()

    result = corpus.to_dict()

    assert result["id"] == "corpus-1"


def test_to_dict_contains_metadata():
    corpus = make_corpus()

    result = corpus.to_dict()

    assert "metadata" in result


def test_to_dict_contains_documents():
    corpus = make_corpus()
    corpus.add_document(make_document())

    result = corpus.to_dict()

    assert "documents" in result
    assert len(result["documents"]) == 1


def test_repr_contains_corpus_information():
    corpus = make_corpus()

    representation = repr(corpus)

    assert "Corpus" in representation
    assert "corpus-1" in representation
