
from __future__ import annotations

import pytest

from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_format import SourceFormat
from SanskritAI.acquisition.models.source_type import SourceType
from SanskritAI.acquisition.repositories.default_source_repository import (
    DefaultSourceRepository,
)


def make_source(
    identifier: str = "test-source",
) -> CorpusSource:
    """
    Creates the smallest valid CorpusSource used by the tests.

    The helper intentionally follows the canonical CorpusSource
    constructor:
        source_id
        name
        source_type
        source_format
    """

    return CorpusSource(
        source_id=identifier,
        name="Test Source",
        source_type=SourceType.CORPUS,
        source_format=SourceFormat.TEXT,
    )


def test_repository_starts_empty():
    repository = DefaultSourceRepository()

    assert len(repository) == 0


def test_add_registers_source():
    repository = DefaultSourceRepository()

    source = make_source()

    repository.add(source)

    assert len(repository) == 1
    assert repository.get("test-source") is source


def test_add_duplicate_identifier_is_rejected():
    repository = DefaultSourceRepository()

    repository.add(
        make_source("same-source")
    )

    with pytest.raises((ValueError, KeyError)):
        repository.add(
            make_source("same-source")
        )


def test_get_returns_registered_source():
    repository = DefaultSourceRepository()

    source = make_source("amarakosha")

    repository.add(source)

    result = repository.get("amarakosha")

    assert result is source


def test_get_returns_none_for_unknown_source():
    repository = DefaultSourceRepository()

    assert repository.get("unknown") is None


def test_exists_returns_false_for_unknown_source():
    repository = DefaultSourceRepository()

    assert repository.exists("missing-source") is False


def test_exists_returns_true_for_registered_source():
    repository = DefaultSourceRepository()

    repository.add(
        make_source("source-a")
    )

    assert repository.exists("source-a") is True


def test_all_returns_registered_sources():
    repository = DefaultSourceRepository()

    source_a = make_source("source-a")
    source_b = make_source("source-b")

    repository.add(source_a)
    repository.add(source_b)

    result = repository.all()

    assert source_a in result
    assert source_b in result
    assert len(result) == 2


def test_all_returns_immutable_snapshot():
    repository = DefaultSourceRepository()

    source = make_source()

    repository.add(source)

    result = repository.all()

    assert isinstance(result, tuple)

    with pytest.raises(AttributeError):
        result.append(source)


def test_remove_returns_removed_source():
    repository = DefaultSourceRepository()

    source = make_source()

    repository.add(source)

    removed = repository.remove("test-source")

    assert removed is source
    assert repository.get("test-source") is None
    assert len(repository) == 0


def test_remove_unknown_returns_none():
    repository = DefaultSourceRepository()

    assert repository.remove("missing-source") is None


def test_clear_removes_all_sources():
    repository = DefaultSourceRepository()

    repository.add(
        make_source("source-a")
    )

    repository.add(
        make_source("source-b")
    )

    repository.clear()

    assert len(repository) == 0
    assert repository.all() == ()


def test_repository_is_iterable():
    repository = DefaultSourceRepository()

    source_a = make_source("source-a")
    source_b = make_source("source-b")

    repository.add(source_a)
    repository.add(source_b)

    result = tuple(repository)

    assert result == (
        source_a,
        source_b,
    )


def test_contains_protocol():
    repository = DefaultSourceRepository()

    repository.add(
        make_source("source-a")
    )

    assert "source-a" in repository
    assert "missing-source" not in repository


def test_len_protocol():
    repository = DefaultSourceRepository()

    assert len(repository) == 0

    repository.add(
        make_source("source-a")
    )

    assert len(repository) == 1
