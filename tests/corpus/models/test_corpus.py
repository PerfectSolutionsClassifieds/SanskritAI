from __future__ import annotations

"""
SanskritAI
==========

Corpus Unit Tests

Tests the structural and domain contract of Corpus.

Corpus is the root ContainerNode of the canonical corpus
hierarchy:

    Corpus
        Document
            Section
                Verse
                    Paragraph
                        Line
                            Token

The tests verify both:

1. Corpus-specific document semantics.
2. Structural convergence with ContainerNode.

Version
-------
v0.3.1
"""

from SanskritAI.common.identifiers.corpus_id import CorpusId
from SanskritAI.corpus.models.container_node import ContainerNode
from SanskritAI.corpus.models.corpus import Corpus
from SanskritAI.corpus.models.corpus_metadata import CorpusMetadata
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.document_metadata import DocumentMetadata


# =============================================================
# Test Helpers
# =============================================================


def make_corpus(
    identifier: str = "corpus-1",
) -> Corpus:

    return Corpus(
        id=CorpusId(identifier),
        metadata=CorpusMetadata(),
    )


def make_document(
    identifier: str = "document-1",
) -> Document:

    return Document(
        identifier=identifier,
        metadata=DocumentMetadata(),
    )


# =============================================================
# Construction
# =============================================================


def test_corpus_stores_identifier():
    corpus = make_corpus()

    assert corpus.id == CorpusId("corpus-1")


def test_corpus_identifier_aliases_id():
    corpus = make_corpus()

    assert corpus.identifier == corpus.id


def test_corpus_stores_metadata():
    metadata = CorpusMetadata()

    corpus = Corpus(
        id=CorpusId("corpus-1"),
        metadata=metadata,
    )

    assert corpus.metadata is metadata


# =============================================================
# Structural Convergence
# =============================================================


def test_corpus_is_a_container_node():
    corpus = make_corpus()

    assert isinstance(corpus, ContainerNode)


def test_corpus_uses_container_node_children():
    corpus = make_corpus()

    assert corpus.children is not None


def test_documents_alias_children():
    corpus = make_corpus()

    assert corpus.documents is corpus.children


def test_corpus_starts_without_documents():
    corpus = make_corpus()

    assert corpus.documents == []
    assert corpus.document_count == 0
    assert corpus.child_count == 0


def test_document_count_aliases_child_count():
    corpus = make_corpus()

    document = make_document()

    corpus.add_document(document)

    assert corpus.document_count == corpus.child_count


# =============================================================
# Document Management
# =============================================================


def test_add_document():
    corpus = make_corpus()
    document = make_document()

    corpus.add_document(document)

    assert corpus.documents == [document]
    assert corpus.document_count == 1
    assert corpus.child_count == 1


def test_remove_document():
    corpus = make_corpus()
    document = make_document()

    corpus.add_document(document)
    corpus.remove_document(document)

    assert corpus.documents == []
    assert corpus.document_count == 0
    assert corpus.child_count == 0


def test_clear_documents():
    corpus = make_corpus()

    documents = [
        make_document("document-1"),
        make_document("document-2"),
        make_document("document-3"),
    ]

    for document in documents:
        corpus.add_document(document)

    corpus.clear_documents()

    assert corpus.documents == []
    assert corpus.document_count == 0
    assert corpus.child_count == 0


# =============================================================
# First / Last
# =============================================================


def test_first_document_aliases_first_child():
    corpus = make_corpus()

    first = make_document("document-1")
    second = make_document("document-2")

    corpus.add_document(first)
    corpus.add_document(second)

    assert corpus.first_document is first
    assert corpus.first_child is first


def test_last_document_aliases_last_child():
    corpus = make_corpus()

    first = make_document("document-1")
    second = make_document("document-2")

    corpus.add_document(first)
    corpus.add_document(second)

    assert corpus.last_document is second
    assert corpus.last_child is second


def test_first_and_last_document_are_none_when_empty():
    corpus = make_corpus()

    assert corpus.first_document is None
    assert corpus.last_document is None


# =============================================================
# Insertion Order
# =============================================================


def test_documents_preserve_insertion_order():
    corpus = make_corpus()

    documents = [
        make_document("document-1"),
        make_document("document-2"),
        make_document("document-3"),
    ]

    for document in documents:
        corpus.add_document(document)

    assert corpus.documents == documents


def test_children_preserve_same_insertion_order_as_documents():
    corpus = make_corpus()

    documents = [
        make_document("document-1"),
        make_document("document-2"),
        make_document("document-3"),
    ]

    for document in documents:
        corpus.add_document(document)

    assert list(corpus.children) == documents
    assert list(corpus.documents) == documents


# =============================================================
# Container Protocol
# =============================================================


def test_corpus_supports_iteration():
    corpus = make_corpus()

    first = make_document("document-1")
    second = make_document("document-2")

    corpus.add_document(first)
    corpus.add_document(second)

    assert list(corpus) == [first, second]


def test_corpus_supports_indexing():
    corpus = make_corpus()

    first = make_document("document-1")
    second = make_document("document-2")

    corpus.add_document(first)
    corpus.add_document(second)

    assert corpus[0] is first
    assert corpus[1] is second


def test_corpus_length_aliases_document_count():
    corpus = make_corpus()

    documents = [
        make_document("document-1"),
        make_document("document-2"),
    ]

    for document in documents:
        corpus.add_document(document)

    assert len(corpus) == corpus.document_count
    assert len(corpus) == corpus.child_count


# =============================================================
# Identity Contract
# =============================================================


def test_corpus_id_is_read_only():
    corpus = make_corpus()

    try:
        corpus.id = CorpusId("corpus-2")
    except AttributeError:
        pass
    else:
        raise AssertionError("Corpus.id must be read-only")


def test_corpus_identifier_is_read_only():
    corpus = make_corpus()

    try:
        corpus.identifier = CorpusId("corpus-2")
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "Corpus.identifier must be read-only"
        )


def test_corpus_identity_is_type_safe():
    corpus_a = make_corpus("corpus-1")
    corpus_b = make_corpus("corpus-1")

    assert corpus_a == corpus_b
    assert hash(corpus_a) == hash(corpus_b)


def test_corpus_different_identifiers_are_not_equal():
    corpus_a = make_corpus("corpus-1")
    corpus_b = make_corpus("corpus-2")

    assert corpus_a != corpus_b


# =============================================================
# Representation
# =============================================================


def test_corpus_repr_contains_identifier():
    corpus = make_corpus("corpus-1")

    representation = repr(corpus)

    assert "corpus-1" in representation


def test_corpus_repr_contains_document_count():
    corpus = make_corpus()

    corpus.add_document(
        make_document("document-1")
    )

    representation = repr(corpus)

    assert "documents=1" in representation
