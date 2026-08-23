
"""
SanskritAI
==========

Unit tests:
    services.importers.amarakosha_parser

Purpose
-------
Focused contract tests for the Amarakośa parser's reconciliation
with the canonical ImportResult model.

These tests intentionally verify the PUBLIC parser -> ImportResult
boundary rather than internal implementation details.

Contract under test
-------------------

    AmarakoshaParser
          |
          v
    ImportResultBuilder
          |
          v
    models.imports.ImportResult

The tests protect:

    * canonical ImportResult type
    * ImportStatus lifecycle
    * imported_object reconciliation
    * ImportStatistics reconciliation
    * warning handling
    * fatal-error handling
    * parse_file() public API
    * canonical builder method usage
    * removal of legacy SUCCESS semantics
"""

from __future__ import annotations

from pathlib import Path

import pytest

from SanskritAI.models.imports import (
    ImportResult,
    ImportStatus,
)

from SanskritAI.services.importers.amarakosha_parser import (
    AmarakoshaParser,
)


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def parser() -> AmarakoshaParser:
    """
    Fresh Amarakośa parser for each test.
    """

    return AmarakoshaParser()


@pytest.fixture
def minimal_valid_text() -> str:
    """
    Minimal structurally valid Amarakośa input.

    LineClassifier recognizes:

        काण्ड -> KANDA
        वर्ग  -> VARGA
        1     -> VERSE
    """

    return "\n".join(
        [
            "स्वर्गकाण्ड",
            "स्वर्गवर्ग",
            "1",
        ]
    )


# ============================================================
# Result Type
# ============================================================


def test_parse_text_returns_canonical_import_result(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    The parser must return the canonical ImportResult model.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert isinstance(
        result,
        ImportResult,
    )


# ============================================================
# Successful Import
# ============================================================


def test_successful_parse_returns_completed_status(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    A valid Amarakośa parse must complete successfully.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert result.status is ImportStatus.COMPLETED
    assert result.successful is True


def test_successful_parse_has_no_errors(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    A valid parse must not produce import errors.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert result.error_count == 0
    assert result.has_errors is False


# ============================================================
# Imported Object Reconciliation
# ============================================================


def test_successful_parse_reconciles_imported_object(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    The parser must place the constructed Amarakośa object into
    ImportResult.imported_object.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert result.imported_object is not None

    # The parser context should contain the exact same object.
    assert result.imported_object is parser.context.book


def test_imported_object_is_not_lost_during_result_build(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    ImportResultBuilder must preserve the parser's domain object.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert result.imported_object is parser.context.book


# ============================================================
# Statistics Reconciliation
# ============================================================


def test_statistics_are_reconciled_from_parser_context(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    Parser statistics must be propagated into ImportResult.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert result.statistics is parser.context.statistics


def test_statistics_contain_expected_structural_counts(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    Minimal input should produce:

        1 Kanda
        1 Varga
        1 Verse
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert result.statistics.kandas == 1
    assert result.statistics.vargas == 1
    assert result.statistics.verses == 1


# ============================================================
# Warning Reconciliation
# ============================================================


def test_unknown_line_produces_warning(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    Unknown lexical input is handled as a recoverable warning.
    """

    text = "\n".join(
        [
            minimal_valid_text,
            "THIS_IS_AN_UNKNOWN_LINE",
        ]
    )

    result = parser.parse_text(
        text,
    )

    assert result.warning_count >= 1
    assert result.has_warnings is True


def test_warning_does_not_make_import_unsuccessful(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    Recoverable warnings must not make a completed import
    unsuccessful.

    The final lifecycle state is expected to distinguish
    successful-with-warnings from failure.
    """

    text = "\n".join(
        [
            minimal_valid_text,
            "THIS_IS_AN_UNKNOWN_LINE",
        ]
    )

    result = parser.parse_text(
        text,
    )

    assert result.successful is True
    assert result.status is ImportStatus.COMPLETED


# ============================================================
# Structural Warning Path
# ============================================================


def test_structural_violation_is_recoverable(
    parser: AmarakoshaParser,
) -> None:
    """
    A structurally misplaced Varga should be captured as a
    parser warning rather than escaping as an exception.
    """

    result = parser.parse_text(
        "स्वर्गवर्ग",
    )

    assert isinstance(
        result,
        ImportResult,
    )

    assert result.warning_count >= 1


# ============================================================
# Fatal/System Error Path
# ============================================================


def test_parser_converts_unexpected_exception_to_failed_result(
    parser: AmarakoshaParser,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Unexpected parser exceptions must be converted into the
    canonical FAILED ImportResult rather than escaping through
    the public parse API.
    """

    def explode(lines: list[str]) -> None:
        raise RuntimeError(
            "synthetic parser failure",
        )

    monkeypatch.setattr(
        parser,
        "_engine_loop",
        explode,
    )

    result = parser.parse_text(
        "स्वर्गकाण्ड",
    )

    assert isinstance(
        result,
        ImportResult,
    )

    assert result.status is ImportStatus.FAILED
    assert result.successful is False
    assert result.error_count >= 1


def test_failed_result_contains_diagnostic(
    parser: AmarakoshaParser,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    A system failure must leave a structured diagnostic in the
    returned ImportResult.
    """

    def explode(lines: list[str]) -> None:
        raise RuntimeError(
            "synthetic parser failure",
        )

    monkeypatch.setattr(
        parser,
        "_engine_loop",
        explode,
    )

    result = parser.parse_text(
        "स्वर्गकाण्ड",
    )

    assert result.error_count >= 1
    assert len(result.errors) >= 1


# ============================================================
# parse_file() Public API
# ============================================================


def test_parse_file_returns_canonical_import_result(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
    tmp_path: Path,
) -> None:
    """
    parse_file() must use the same canonical ImportResult
    contract as parse_text().
    """

    source = tmp_path / "amarakosha.txt"

    source.write_text(
        minimal_valid_text,
        encoding="utf-8",
    )

    result = parser.parse_file(
        source,
    )

    assert isinstance(
        result,
        ImportResult,
    )

    assert result.status is ImportStatus.COMPLETED
    assert result.successful is True
    assert result.imported_object is not None


def test_parse_file_rejects_unsupported_extension(
    parser: AmarakoshaParser,
    tmp_path: Path,
) -> None:
    """
    Amarakośa parser currently accepts .txt input only.
    """

    source = tmp_path / "amarakosha.xml"

    source.write_text(
        "स्वर्गकाण्ड",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="not supported",
    ):
        parser.parse_file(
            source,
        )


def test_parse_file_rejects_missing_file(
    parser: AmarakoshaParser,
    tmp_path: Path,
) -> None:
    """
    Missing input files must raise FileNotFoundError.
    """

    source = tmp_path / "missing.txt"

    with pytest.raises(
        FileNotFoundError,
    ):
        parser.parse_file(
            source,
        )


# ============================================================
# Canonical Status Vocabulary
# ============================================================


def test_amarakosha_parser_uses_canonical_status_vocabulary() -> None:
    """
    ImportStatus.SUCCESS must not exist in the canonical
    lifecycle vocabulary.

    COMPLETED is the canonical successful terminal state.
    """

    assert not hasattr(
        ImportStatus,
        "SUCCESS",
    )

    assert ImportStatus.COMPLETED.is_success is True
    assert (
        ImportStatus.COMPLETED_WITH_WARNINGS.is_success
        is True
    )

    assert ImportStatus.FAILED.is_success is False
    assert ImportStatus.CANCELLED.is_success is False


# ============================================================
# Result Lifecycle
# ============================================================


def test_successful_result_is_terminal(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    A completed Amarakośa import must return a terminal status.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert result.status.is_finished is True


def test_statistics_timing_is_started(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    ImportResult construction must initialize statistics timing.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert result.statistics.started_at > 0.0


# ============================================================
# Public Result Contract
# ============================================================


def test_result_string_representation_is_available(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    The canonical ImportResult representation should remain
    available to callers.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    text = str(result)

    assert "Completed" in text
    assert "errors=" in text
    assert "warnings=" in text
    assert "units=" in text


# ============================================================
# Regression Guard
# ============================================================


def test_parser_context_remains_available_after_parse(
    parser: AmarakoshaParser,
    minimal_valid_text: str,
) -> None:
    """
    Parser context remains available for diagnostics and
    inspection after parsing.
    """

    result = parser.parse_text(
        minimal_valid_text,
    )

    assert parser.context is not None
    assert result.imported_object is parser.context.book
    assert result.statistics is parser.context.statistics
