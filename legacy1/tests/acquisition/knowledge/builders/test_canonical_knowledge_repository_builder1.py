
from __future__ import annotations

from unittest.mock import Mock

import pytest

from SanskritAI.acquisition.knowledge.builders.canonical_knowledge_repository_builder import (
    CanonicalKnowledgeRepositoryBuilder,
)
from SanskritAI.acquisition.knowledge.builders.canonical_index_builder import (
    CanonicalIndexBuilder,
)
from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)


# =========================================================
# Helpers
# =========================================================


def make_lexicon() -> CanonicalLexicon:
    return CanonicalLexicon()


def make_repository() -> CanonicalKnowledgeRepository:

    return CanonicalKnowledgeRepository()


def make_index_builder() -> CanonicalIndexBuilder:

    return CanonicalIndexBuilder(
        headword_index=Mock(),
        lemma_index=Mock(),
        context_index=Mock(),
        source_index=Mock(),
    )


def make_builder(
    repository=None,
    index_builder=None,
):

    return CanonicalKnowledgeRepositoryBuilder(
        repository=(
            repository
            if repository is not None
            else make_repository()
        ),
        index_builder=(
            index_builder
            if index_builder is not None
            else make_index_builder()
        ),
    )


# =========================================================
# Construction
# =========================================================


def test_builder_can_be_constructed():

    builder = make_builder()

    assert isinstance(
        builder,
        CanonicalKnowledgeRepositoryBuilder,
    )


def test_builder_retains_repository():

    repository = make_repository()

    builder = make_builder(
        repository=repository,
    )

    assert builder.repository is repository


def test_builder_retains_index_builder():

    index_builder = make_index_builder()

    builder = make_builder(
        index_builder=index_builder,
    )

    assert builder.index_builder is index_builder


# =========================================================
# Build
# =========================================================


def test_build_returns_repository():

    repository = make_repository()

    builder = make_builder(
        repository=repository,
    )

    result = builder.build(())

    assert result is repository


def test_build_populates_lexical_registry():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    lexicon = make_lexicon()

    builder.build(
        (lexicon,)
    )

    assert (
        repository.lexical_registry.all()
    )


def test_build_synchronizes_indexes():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    lexicon = make_lexicon()

    builder.build(
        (lexicon,)
    )

    index_builder.build.assert_called_once_with(
        repository.lexical_registry.all()
    )


# =========================================================
# Multiple Lexicons
# =========================================================


def test_build_registers_all_lexicons():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    first = make_lexicon()
    second = make_lexicon()

    builder.build(
        (first, second)
    )

    registered = (
        repository.lexical_registry.all()
    )

    assert first in registered
    assert second in registered


# =========================================================
# Rebuild Semantics
# =========================================================


def test_build_clears_previous_repository_state():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    first = make_lexicon()

    builder.build(
        (first,)
    )

    second = make_lexicon()

    builder.build(
        (second,)
    )

    registered = (
        repository.lexical_registry.all()
    )

    assert first not in registered
    assert second in registered


def test_build_synchronizes_indexes_after_rebuild():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    first = make_lexicon()

    builder.build(
        (first,)
    )

    second = make_lexicon()

    builder.build(
        (second,)
    )

    assert (
        index_builder.build.call_count == 2
    )


# =========================================================
# Incremental Addition
# =========================================================


def test_add_lexicon_registers_lexicon():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    lexicon = make_lexicon()

    builder.add_lexicon(
        lexicon
    )

    assert (
        lexicon
        in repository.lexical_registry.all()
    )


def test_add_lexicon_resynchronizes_indexes():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    lexicon = make_lexicon()

    builder.add_lexicon(
        lexicon
    )

    index_builder.build.assert_called_once_with(
        repository.lexical_registry.all()
    )


def test_add_multiple_lexicons_is_incremental():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    first = make_lexicon()
    second = make_lexicon()

    builder.add_lexicon(first)
    builder.add_lexicon(second)

    registered = (
        repository.lexical_registry.all()
    )

    assert first in registered
    assert second in registered

    assert index_builder.build.call_count == 2


# =========================================================
# Clear
# =========================================================


def test_clear_clears_lexical_registry():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    lexicon = make_lexicon()

    builder.build(
        (lexicon,)
    )

    builder.clear()

    assert (
        repository.lexical_registry.all()
        == ()
    )


def test_clear_clears_lemma_registry():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    builder.clear()

    assert (
        repository.lemma_registry.all()
        == ()
    )


def test_clear_clears_source_registry():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    builder.clear()

    assert (
        repository.source_registry.all()
        == ()
    )


def test_clear_clears_knowledge_index():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    builder.clear()

    assert (
        repository.knowledge_index.summary()
        == {
            "headwords": 0,
            "lemmas": 0,
            "contexts": 0,
            "sources": 0,
        }
    )


# =========================================================
# Diagnostics
# =========================================================


def test_summary_delegates_to_repository():

    repository = make_repository()

    index_builder = make_index_builder()

    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )

    summary = builder.summary()

    assert summary == {
        "repository": repository.summary(),
    }


def test_string_representation_contains_builder_name():

    builder = make_builder()

    text = str(builder)

    assert (
        "CanonicalKnowledgeRepositoryBuilder"
        in text
    )
