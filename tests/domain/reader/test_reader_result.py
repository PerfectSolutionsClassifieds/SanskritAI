from __future__ import annotations

"""
SanskritAI
==========

ReaderResult Tests

Verifies the immutable ReaderResult aggregate that bridges the
Reader Domain and the Resolution Domain.

The tests intentionally use lightweight placeholder objects for
resolution results because ReaderResult is an aggregate/projection
object and should not require concrete kernel implementations in
order to establish its own contract.

Version
-------
v1.0.0
"""

from dataclasses import FrozenInstanceError
from types import SimpleNamespace

import pytest

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_result import (
    ReaderResult,
)


# =============================================================
# Fixtures
# =============================================================


@pytest.fixture
def position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )


@pytest.fixture
def subject():
    return SimpleNamespace(
        identifier="word-1",
        text="धर्मः",
    )


@pytest.fixture
def empty_result(
    position,
    subject,
):
    return ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
    )


# =============================================================
# Construction
# =============================================================


def test_reader_result_preserves_identifier(
    empty_result,
):
    assert (
        empty_result.identifier
        == "reader-result-1"
    )


def test_reader_result_preserves_position(
    empty_result,
    position,
):
    assert empty_result.position is position


def test_reader_result_preserves_subject(
    empty_result,
    subject,
):
    assert empty_result.subject is subject


# =============================================================
# Empty Resolution State
# =============================================================


def test_empty_result_has_no_lexical_result(
    empty_result,
):
    assert not empty_result.lexical_available


def test_empty_result_has_no_morphology_result(
    empty_result,
):
    assert not empty_result.morphology_available


def test_empty_result_has_no_sandhi_result(
    empty_result,
):
    assert not empty_result.sandhi_available


def test_empty_result_has_no_samasa_result(
    empty_result,
):
    assert not empty_result.samasa_available


def test_empty_result_has_no_semantic_result(
    empty_result,
):
    assert not empty_result.semantic_available


def test_empty_result_has_no_pragmatics(
    empty_result,
):
    assert not empty_result.pragmatics_available


def test_empty_result_has_no_commentary(
    empty_result,
):
    assert not empty_result.commentary_available


# =============================================================
# Empty Completion State
# =============================================================


def test_empty_result_has_zero_completed_stages(
    empty_result,
):
    assert (
        empty_result.completed_stage_count
        == 0
    )


def test_total_stage_count_is_seven(
    empty_result,
):
    assert (
        empty_result.total_stage_count
        == 7
    )


def test_empty_result_completion_ratio_is_zero(
    empty_result,
):
    assert (
        empty_result.completion_ratio
        == 0.0
    )


def test_empty_result_is_not_complete(
    empty_result,
):
    assert not empty_result.is_complete


# =============================================================
# Individual Resolution Stages
# =============================================================


def test_lexical_result_counts_as_completed_stage(
    position,
    subject,
):
    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        lexical_result=object(),
    )

    assert result.lexical_available

    assert (
        result.completed_stage_count
        == 1
    )

    assert (
        result.completion_ratio
        == pytest.approx(1 / 7)
    )

    assert not result.is_complete


def test_morphology_result_counts_as_completed_stage(
    position,
    subject,
):
    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        morphology_result=object(),
    )

    assert result.morphology_available

    assert (
        result.completed_stage_count
        == 1
    )


def test_sandhi_result_counts_as_completed_stage(
    position,
    subject,
):
    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        sandhi_result=object(),
    )

    assert result.sandhi_available

    assert (
        result.completed_stage_count
        == 1
    )


def test_samasa_result_counts_as_completed_stage(
    position,
    subject,
):
    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        samasa_result=object(),
    )

    assert result.samasa_available

    assert (
        result.completed_stage_count
        == 1
    )


def test_semantic_result_counts_as_completed_stage(
    position,
    subject,
):
    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        semantic_result=object(),
    )

    assert result.semantic_available

    assert (
        result.completed_stage_count
        == 1
    )


def test_pragmatics_counts_as_completed_stage(
    position,
    subject,
):
    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        pragmatics=object(),
    )

    assert result.pragmatics_available

    assert (
        result.completed_stage_count
        == 1
    )


def test_commentary_counts_as_completed_stage(
    position,
    subject,
):
    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        commentary=object(),
    )

    assert result.commentary_available

    assert (
        result.completed_stage_count
        == 1
    )


# =============================================================
# Complete Resolution State
# =============================================================


def test_all_resolution_stages_produce_complete_result(
    position,
    subject,
):
    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        lexical_result=object(),
        morphology_result=object(),
        sandhi_result=object(),
        samasa_result=object(),
        semantic_result=object(),
        pragmatics=object(),
        commentary=object(),
    )

    assert result.lexical_available
    assert result.morphology_available
    assert result.sandhi_available
    assert result.samasa_available
    assert result.semantic_available
    assert result.pragmatics_available
    assert result.commentary_available

    assert (
        result.completed_stage_count
        == 7
    )

    assert (
        result.total_stage_count
        == 7
    )

    assert (
        result.completion_ratio
        == 1.0
    )

    assert result.is_complete


# =============================================================
# Cross References
# =============================================================


def test_empty_result_has_no_cross_references(
    empty_result,
):
    assert not empty_result.has_cross_references

    assert (
        empty_result.cross_reference_count
        == 0
    )


def test_cross_references_are_counted(
    position,
    subject,
):
    references = (
        "sloka-2",
        "sloka-3",
    )

    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        cross_references=references,
    )

    assert result.has_cross_references

    assert (
        result.cross_reference_count
        == 2
    )


# =============================================================
# Canonical Sources
# =============================================================


def test_empty_result_has_no_canonical_sources(
    empty_result,
):
    assert not empty_result.has_canonical_sources

    assert (
        empty_result.canonical_source_count
        == 0
    )


def test_canonical_sources_are_counted(
    position,
    subject,
):
    sources = (
        "amarakosha",
        "vacaspatiyam",
        "shabdakalpadruma",
    )

    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        canonical_sources=sources,
    )

    assert result.has_canonical_sources

    assert (
        result.canonical_source_count
        == 3
    )


# =============================================================
# Metadata
# =============================================================


def test_empty_result_has_no_metadata(
    empty_result,
):
    assert not empty_result.has_metadata


def test_metadata_is_available(
    position,
    subject,
):
    result = ReaderResult(
        identifier="reader-result-1",
        position=position,
        subject=subject,
        metadata={
            "source": "test-edition",
            "page": 42,
        },
    )

    assert result.has_metadata

    assert (
        result.get_metadata("source")
        == "test-edition"
    )

    assert (
        result.get_metadata("page")
        == 42
    )


def test_missing_metadata_returns_default(
    empty_result,
):
    assert (
        empty_result.get_metadata(
            "missing",
            "fallback",
        )
        == "fallback"
    )


# =============================================================
# Display
# =============================================================


def test_display_name(
    empty_result,
):
    assert (
        empty_result.display_name
        == "Reader Result"
    )


def test_display_text_uses_subject(
    empty_result,
    subject,
):
    assert (
        empty_result.display_text
        == str(subject)
    )


def test_display_description(
    empty_result,
):
    assert (
        "Reader Domain"
        in empty_result.display_description
        or
        "linguistic"
        in empty_result.display_description.lower()
    )


def test_string_representation_uses_display_text(
    empty_result,
):
    assert (
        str(empty_result)
        == empty_result.display_text
    )


# =============================================================
# Immutability
# =============================================================


def test_reader_result_is_immutable(
    empty_result,
):
    with pytest.raises(
        FrozenInstanceError,
    ):
        empty_result.identifier = (
            "changed"
        )


def test_reader_result_position_is_not_reassignable(
    empty_result,
):
    with pytest.raises(
        FrozenInstanceError,
    ):
        empty_result.position = None


def test_reader_result_subject_is_not_reassignable(
    empty_result,
):
    with pytest.raises(
        FrozenInstanceError,
    ):
        empty_result.subject = None


# =============================================================
# Structural Contract
# =============================================================


def test_reader_result_has_expected_resolution_fields(
    empty_result,
):
    assert hasattr(
        empty_result,
        "lexical_result",
    )

    assert hasattr(
        empty_result,
        "morphology_result",
    )

    assert hasattr(
        empty_result,
        "sandhi_result",
    )

    assert hasattr(
        empty_result,
        "samasa_result",
    )

    assert hasattr(
        empty_result,
        "semantic_result",
    )

    assert hasattr(
        empty_result,
        "pragmatics",
    )

    assert hasattr(
        empty_result,
        "commentary",
    )


def test_reader_result_has_reference_fields(
    empty_result,
):
    assert hasattr(
        empty_result,
        "cross_references",
    )

    assert hasattr(
        empty_result,
        "canonical_sources",
    )

    assert hasattr(
        empty_result,
        "metadata",
    )
