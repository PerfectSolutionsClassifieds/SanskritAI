from __future__ import annotations

from unittest.mock import Mock

import pytest

from SanskritAI.acquisition.knowledge.builders.canonical_knowledge_repository_builder import (
    CanonicalKnowledgeRepositoryBuilder,
    _ensure_lexical_repository_has_all,
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


def make_lexicon(
    identifier: str = "test-lexicon",
    name: str = "Test Lexicon",
    version: str = "1.0",
) -> CanonicalLexicon:
    return CanonicalLexicon(
        identifier=identifier,
        name=name,
        version=version,
    )


def make_repository() -> CanonicalKnowledgeRepository:
    repo = CanonicalKnowledgeRepository()
    if hasattr(repo, "lexical_repository"):
        _ensure_lexical_repository_has_all(repo.lexical_repository)
    return repo


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
    repo = repository if repository is not None else make_repository()
    idx = index_builder if index_builder is not None else make_index_builder()
    return CanonicalKnowledgeRepositoryBuilder(
        repository=repo,
        index_builder=idx,
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
    result = builder.build(
        (),
    )
    assert result is repository


def test_build_populates_lexical_repository():
    repository = make_repository()
    index_builder = make_index_builder()
    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )
    lexicon = make_lexicon()
    builder.build(
        (lexicon,),
    )
    assert lexicon in repository.lexical_repository.all()


def test_build_synchronizes_indexes():
    repository = make_repository()
    index_builder = make_index_builder()
    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )
    lexicon = make_lexicon()
    builder.build(
        (lexicon,),
    )
    index_builder.build.assert_called_once_with(
        repository.lexical_repository.all()
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
    first = make_lexicon(
        identifier="lexicon-1",
        name="First Lexicon",
    )
    second = make_lexicon(
        identifier="lexicon-2",
        name="Second Lexicon",
    )
    builder.build(
        (
            first,
            second,
        )
    )
    registered = repository.lexical_repository.all()
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
    first = make_lexicon(
        identifier="lexicon-1",
        name="First Lexicon",
    )
    builder.build(
        (first,),
    )
    second = make_lexicon(
        identifier="lexicon-2",
        name="Second Lexicon",
    )
    builder.build(
        (second,),
    )
    registered = repository.lexical_repository.all()
    assert first not in registered
    assert second in registered


def test_build_synchronizes_indexes_after_rebuild():
    repository = make_repository()
    index_builder = make_index_builder()
    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )
    first = make_lexicon(
        identifier="lexicon-1",
        name="First Lexicon",
    )
    second = make_lexicon(
        identifier="lexicon-2",
        name="Second Lexicon",
    )
    builder.build(
        (first,),
    )
    builder.build(
        (second,),
    )
    assert index_builder.build.call_count == 2


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
        lexicon,
    )
    assert lexicon in repository.lexical_repository.all()


def test_add_lexicon_resynchronizes_indexes():
    repository = make_repository()
    index_builder = make_index_builder()
    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )
    lexicon = make_lexicon()
    builder.add_lexicon(
        lexicon,
    )
    index_builder.build.assert_called_once_with(
        repository.lexical_repository.all()
    )


def test_add_multiple_lexicons_is_incremental():
    repository = make_repository()
    index_builder = make_index_builder()
    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )
    first = make_lexicon(
        identifier="lexicon-1",
        name="First Lexicon",
    )
    second = make_lexicon(
        identifier="lexicon-2",
        name="Second Lexicon",
    )
    builder.add_lexicon(
        first,
    )
    builder.add_lexicon(
        second,
    )
    registered = repository.lexical_repository.all()
    assert first in registered
    assert second in registered
    assert index_builder.build.call_count == 2


# =========================================================
# Clear
# =========================================================


def test_clear_clears_lexical_repository():
    repository = make_repository()
    index_builder = make_index_builder()
    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )
    lexicon = make_lexicon()
    builder.build(
        (lexicon,),
    )
    builder.clear()
    assert (
        repository.lexical_repository.all() == ()
        or len(repository.lexical_repository.all()) == 0
    )


def test_clear_clears_indexes():
    repository = make_repository()
    index_builder = make_index_builder()
    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )
    builder.clear()
    index_builder.headword_index.clear.assert_called_once()
    index_builder.lemma_index.clear.assert_called_once()
    index_builder.context_index.clear.assert_called_once()
    index_builder.source_index.clear.assert_called_once()


# =========================================================
# Diagnostics
# =========================================================


def test_summary_delegates_to_repository():
    repository = Mock()
    repository.summary.return_value = {
        "lexical": 0,
    }
    index_builder = make_index_builder()
    builder = make_builder(
        repository=repository,
        index_builder=index_builder,
    )
    summary = builder.summary()
    assert summary == {
        "repository": {
            "lexical": 0,
        },
    }
    repository.summary.assert_called_once()


def test_string_representation_contains_builder_name():
    builder = make_builder()
    text = str(builder)
    assert "CanonicalKnowledgeRepositoryBuilder" in text
    
