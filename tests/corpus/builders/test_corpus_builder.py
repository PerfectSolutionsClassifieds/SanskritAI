
from __future__ import annotations

import pytest

from SanskritAI.common.identifiers.corpus_id import CorpusId
from SanskritAI.corpus.builders.corpus_builder import CorpusBuilder
from SanskritAI.corpus.models.corpus import Corpus
from SanskritAI.corpus.models.corpus_metadata import CorpusMetadata
from SanskritAI.corpus.models.document import Document


# ============================================================
# Construction / Factory
# ============================================================


def test_create_instance_returns_corpus():
    builder = CorpusBuilder()

    assert isinstance(builder.instance(), Corpus)


def test_create_instance_generates_corpus_id():
    builder = CorpusBuilder()

    assert isinstance(builder.instance().id, CorpusId)


def test_create_instance_initializes_corpus_metadata():
    builder = CorpusBuilder()

    assert isinstance(
        builder.instance().metadata,
        CorpusMetadata,
    )


# ============================================================
# Fluent API
# ============================================================


def test_with_title_is_fluent():
    builder = CorpusBuilder()

    result = builder.with_title("Mahabharata")

    assert result is builder


def test_with_description_is_fluent():
    builder = CorpusBuilder()

    result = builder.with_description(
        "Canonical Sanskrit corpus"
    )

    assert result is builder


def test_with_metadata_is_fluent():
    builder = CorpusBuilder()
    metadata = CorpusMetadata()

    result = builder.with_metadata(metadata)

    assert result is builder


# ============================================================
# Metadata
# ============================================================


def test_with_title_sets_metadata_title():
    builder = CorpusBuilder()

    builder.with_title("Mahabharata")

    assert builder.instance().metadata.title == "Mahabharata"


def test_with_description_sets_metadata_description():
    builder = CorpusBuilder()

    description = "Canonical Sanskrit corpus"

    builder.with_description(description)

    assert (
        builder.instance().metadata.description
        == description
    )


def test_with_metadata_replaces_metadata():
    builder = CorpusBuilder()
    metadata = CorpusMetadata()
    metadata.title = "Injected Corpus"

    builder.with_metadata(metadata)

    assert builder.instance().metadata is metadata
    assert (
        builder.instance().metadata.title
        == "Injected Corpus"
    )


# ============================================================
# Documents
# ============================================================


def test_add_document_is_fluent():
    builder = CorpusBuilder()

    document = Document(
        identifier="document-1",
        metadata=__import__(
            "SanskritAI.corpus.models.document_metadata",
            fromlist=["DocumentMetadata"],
        ).DocumentMetadata(),
    )

    result = builder.add_document(document)

    assert result is builder


def test_add_document_adds_document():
    builder = CorpusBuilder()

    document = Document(
        identifier="document-1",
        metadata=__import__(
            "SanskritAI.corpus.models.document_metadata",
            fromlist=["DocumentMetadata"],
        ).DocumentMetadata(),
    )

    builder.add_document(document)

    assert builder.instance().document_count == 1
    assert builder.instance().first_document is document


def test_add_documents_adds_all_documents():
    builder = CorpusBuilder()

    DocumentMetadata = __import__(
        "SanskritAI.corpus.models.document_metadata",
        fromlist=["DocumentMetadata"],
    ).DocumentMetadata

    documents = [
        Document(
            identifier="document-1",
            metadata=DocumentMetadata(),
        ),
        Document(
            identifier="document-2",
            metadata=DocumentMetadata(),
        ),
        Document(
            identifier="document-3",
            metadata=DocumentMetadata(),
        ),
    ]

    result = builder.add_documents(documents)

    assert result is builder
    assert builder.instance().document_count == 3
    assert list(builder.instance().documents) == documents


# ============================================================
# Validation
# ============================================================


def test_validate_accepts_non_empty_title():
    builder = CorpusBuilder().with_title("Mahabharata")

    builder.validate()


def test_validate_rejects_empty_title():
    builder = CorpusBuilder()

    with pytest.raises(
        ValueError,
        match="Corpus title cannot be empty",
    ):
        builder.validate()


def test_validate_rejects_whitespace_title():
    builder = CorpusBuilder().with_title("   ")

    with pytest.raises(
        ValueError,
        match="Corpus title cannot be empty",
    ):
        builder.validate()


def test_build_requires_valid_title():
    builder = CorpusBuilder()

    with pytest.raises(
        ValueError,
        match="Corpus title cannot be empty",
    ):
        builder.build()


def test_build_returns_corpus():
    builder = CorpusBuilder().with_title(
        "Mahabharata"
    )

    corpus = builder.build()

    assert isinstance(corpus, Corpus)
    assert corpus.metadata.title == "Mahabharata"


# ============================================================
# Build Semantics
# ============================================================


def test_build_returns_independent_copy():
    builder = CorpusBuilder().with_title(
        "Mahabharata"
    )

    built = builder.build()

    builder.with_title("Ramayana")

    assert built.metadata.title == "Mahabharata"
    assert builder.instance().metadata.title == "Ramayana"


def test_build_does_not_replace_builder_instance():
    builder = CorpusBuilder().with_title(
        "Mahabharata"
    )

    instance_before = builder.instance()

    built = builder.build()

    assert builder.instance() is instance_before
    assert built is not instance_before


# ============================================================
# Reset / Reuse
# ============================================================


def test_reset_creates_fresh_corpus():
    builder = CorpusBuilder().with_title(
        "Mahabharata"
    )

    old_instance = builder.instance()

    result = builder.reset()

    assert result is builder
    assert builder.instance() is not old_instance
    assert isinstance(builder.instance(), Corpus)


def test_reset_clears_previous_metadata():
    builder = CorpusBuilder().with_title(
        "Mahabharata"
    )

    builder.reset()

    assert builder.instance().metadata.title == ""


# ============================================================
# from_corpus
# ============================================================


def test_from_corpus_returns_corpus_builder():
    corpus = (
        CorpusBuilder()
        .with_title("Mahabharata")
        .with_description("Epic corpus")
        .build()
    )

    builder = CorpusBuilder.from_corpus(corpus)

    assert isinstance(builder, CorpusBuilder)


def test_from_corpus_copies_corpus_state():
    corpus = (
        CorpusBuilder()
        .with_title("Mahabharata")
        .with_description("Epic corpus")
        .build()
    )

    builder = CorpusBuilder.from_corpus(corpus)

    assert builder.instance().metadata.title == (
        "Mahabharata"
    )

    assert (
        builder.instance().metadata.description
        == "Epic corpus"
    )


def test_from_corpus_preserves_documents():
    DocumentMetadata = __import__(
        "SanskritAI.corpus.models.document_metadata",
        fromlist=["DocumentMetadata"],
    ).DocumentMetadata

    document = Document(
        identifier="document-1",
        metadata=DocumentMetadata(),
    )

    corpus = (
        CorpusBuilder()
        .with_title("Mahabharata")
        .add_document(document)
        .build()
    )

    builder = CorpusBuilder.from_corpus(corpus)

    assert builder.instance().document_count == 1
    assert (
        builder.instance().first_document.id
        == document.id
    )


def test_from_corpus_does_not_alias_original_corpus():
    corpus = (
        CorpusBuilder()
        .with_title("Mahabharata")
        .build()
    )

    builder = CorpusBuilder.from_corpus(corpus)

    builder.with_title("Ramayana")

    assert corpus.metadata.title == "Mahabharata"
    assert builder.instance().metadata.title == "Ramayana"
