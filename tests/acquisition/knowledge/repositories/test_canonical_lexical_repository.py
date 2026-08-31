
from __future__ import annotations

import pytest

from SanskritAI.acquisition.knowledge.repositories.canonical_lexical_repository import (
    CanonicalLexicalRepository,
)
from SanskritAI.acquisition.knowledge.transformers.monier_williams_transformer import (
    CanonicalLexicalRecord,
)


# =========================================================
# Fixtures / Helpers
# =========================================================


def make_record(
    headword: str = "राम",
    source_name: str = "Test Dictionary",
    source_version: str = "1.0",
    record_id: str = "1",
) -> CanonicalLexicalRecord:

    return CanonicalLexicalRecord(
        headword=headword,
        source_name=source_name,
        source_version=source_version,
        source_record_id=record_id,
    )


def make_repository() -> CanonicalLexicalRepository:
    return CanonicalLexicalRepository()


# =========================================================
# Construction
# =========================================================


def test_repository_can_be_constructed():

    repository = make_repository()

    assert isinstance(
        repository,
        CanonicalLexicalRepository,
    )


def test_repository_is_empty_initially():

    repository = make_repository()

    assert len(repository) == 0
    assert repository.headword_count == 0
    assert repository.record_count == 0
    assert repository.headwords == ()
    assert repository.records == ()


# =========================================================
# Add
# =========================================================


def test_add_inserts_record():

    repository = make_repository()
    record = make_record()

    repository.add(record)

    assert repository.contains("राम")
    assert repository.get("राम") == (record,)


def test_add_supports_multiple_records_for_same_headword():

    repository = make_repository()

    first = make_record(
        source_name="Dictionary A",
        record_id="1",
    )

    second = make_record(
        source_name="Dictionary B",
        record_id="2",
    )

    repository.add(first)
    repository.add(second)

    assert repository.headword_count == 1
    assert repository.record_count == 2

    assert repository.get("राम") == (
        first,
        second,
    )


def test_add_supports_multiple_headwords():

    repository = make_repository()

    rama = make_record(
        headword="राम",
        record_id="1",
    )

    hari = make_record(
        headword="हरि",
        record_id="2",
    )

    repository.add(rama)
    repository.add(hari)

    assert repository.headword_count == 2
    assert repository.record_count == 2


# =========================================================
# Add All
# =========================================================


def test_add_all_inserts_all_records():

    repository = make_repository()

    records = (
        make_record("राम", record_id="1"),
        make_record("हरि", record_id="2"),
        make_record("गुरु", record_id="3"),
    )

    repository.add_all(records)

    assert repository.record_count == 3
    assert repository.headword_count == 3


def test_add_all_accepts_general_iterable():

    repository = make_repository()

    records = (
        make_record("राम", record_id="1"),
        make_record("हरि", record_id="2"),
    )

    repository.add_all(
        record for record in records
    )

    assert repository.record_count == 2


# =========================================================
# Lookup
# =========================================================


def test_contains_returns_true_for_existing_headword():

    repository = make_repository()

    repository.add(
        make_record("राम")
    )

    assert repository.contains("राम")


def test_contains_returns_false_for_unknown_headword():

    repository = make_repository()

    assert not repository.contains("राम")


def test_get_returns_all_records_for_headword():

    repository = make_repository()

    first = make_record(
        "राम",
        source_name="A",
        record_id="1",
    )

    second = make_record(
        "राम",
        source_name="B",
        record_id="2",
    )

    repository.add_all(
        (first, second)
    )

    assert repository.get("राम") == (
        first,
        second,
    )


def test_get_unknown_headword_returns_empty_tuple():

    repository = make_repository()

    assert repository.get("unknown") == ()


# =========================================================
# Enumeration
# =========================================================


def test_headwords_are_sorted():

    repository = make_repository()

    repository.add(make_record("हरि"))
    repository.add(make_record("गुरु"))
    repository.add(make_record("राम"))

    assert repository.headwords == (
        "गुरु",
        "राम",
        "हरि",
    )


def test_records_returns_flat_collection():

    repository = make_repository()

    first = make_record(
        "राम",
        record_id="1",
    )

    second = make_record(
        "राम",
        record_id="2",
    )

    third = make_record(
        "हरि",
        record_id="3",
    )

    repository.add_all(
        (first, second, third)
    )

    assert repository.records == (
        first,
        second,
        third,
    )


def test_headword_count_counts_unique_headwords():

    repository = make_repository()

    repository.add(
        make_record("राम", record_id="1")
    )

    repository.add(
        make_record("राम", record_id="2")
    )

    repository.add(
        make_record("हरि", record_id="3")
    )

    assert repository.headword_count == 2


def test_record_count_counts_all_records():

    repository = make_repository()

    repository.add_all(
        (
            make_record("राम", record_id="1"),
            make_record("राम", record_id="2"),
            make_record("हरि", record_id="3"),
        )
    )

    assert repository.record_count == 3


# =========================================================
# Python Protocols
# =========================================================


def test_contains_protocol_delegates_to_contains():

    repository = make_repository()

    repository.add(
        make_record("राम")
    )

    assert "राम" in repository
    assert "हरि" not in repository


def test_len_returns_record_count():

    repository = make_repository()

    repository.add_all(
        (
            make_record("राम", record_id="1"),
            make_record("हरि", record_id="2"),
        )
    )

    assert len(repository) == 2


def test_iteration_yields_all_records():

    repository = make_repository()

    records = (
        make_record("राम", record_id="1"),
        make_record("हरि", record_id="2"),
    )

    repository.add_all(records)

    assert tuple(repository) == records


# =========================================================
# Diagnostics
# =========================================================


def test_summary_reports_repository_statistics():

    repository = make_repository()

    repository.add_all(
        (
            make_record("राम", record_id="1"),
            make_record("राम", record_id="2"),
            make_record("हरि", record_id="3"),
        )
    )

    summary = repository.summary()

    assert summary == {
        "repository": "CanonicalLexicalRepository",
        "unique_headwords": 2,
        "records": 3,
    }


def test_string_representation_contains_counts():

    repository = make_repository()

    repository.add(
        make_record("राम")
    )

    text = str(repository)

    assert "CanonicalLexicalRepository" in text
    assert "1 headwords" in text
    assert "1 records" in text


# =========================================================
# Data Isolation
# =========================================================


def test_get_returns_tuple_not_internal_list():

    repository = make_repository()

    repository.add(
        make_record("राम")
    )

    result = repository.get("राम")

    assert isinstance(result, tuple)


def test_records_returns_tuple():

    repository = make_repository()

    repository.add(
        make_record("राम")
    )

    assert isinstance(
        repository.records,
        tuple,
    )


def test_headwords_returns_tuple():

    repository = make_repository()

    repository.add(
        make_record("राम")
    )

    assert isinstance(
        repository.headwords,
        tuple,
    )
