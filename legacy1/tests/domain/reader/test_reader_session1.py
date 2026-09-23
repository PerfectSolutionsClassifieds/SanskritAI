from __future__ import annotations

"""
SanskritAI
==========

ReaderSession Tests

Verifies:

* session construction
* initial resolution
* current position
* current result
* re-resolution
* forward navigation
* backward navigation
* navigation boundaries
* immutability of ReaderSession

ReaderSession is tested as a stateful façade over ReaderEngine.
"""

from unittest.mock import Mock

import pytest

from SanskritAI.domain.reader.reader_engine import (
    ReaderEngine,
)

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)

from SanskritAI.domain.reader.reader_result import (
    ReaderResult,
)

from SanskritAI.domain.reader.reader_session import (
    ReaderSession,
)


# =============================================================
# Fixtures
# =============================================================


@pytest.fixture
def engine():
    return Mock(
        spec=ReaderEngine,
    )


@pytest.fixture
def position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-1",
    )


@pytest.fixture
def next_position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-2",
    )


@pytest.fixture
def previous_position():
    return ReaderPosition(
        purana_id="purana-1",
        chapter_id="chapter-1",
        sloka_id="sloka-1",
        word_id="word-0",
    )


@pytest.fixture
def result():
    return Mock(
        spec=ReaderResult,
    )


@pytest.fixture
def next_result():
    return Mock(
        spec=ReaderResult,
    )


@pytest.fixture
def previous_result():
    return Mock(
        spec=ReaderResult,
    )


# =============================================================
# Construction
# =============================================================


def test_open_resolves_initial_position(
    engine,
    position,
    result,
):
    engine.resolve.return_value = result

    session = ReaderSession.open(
        engine=engine,
        position=position,
    )

    assert session.engine is engine
    assert session.position is position
    assert session.result is result

    engine.resolve.assert_called_once_with(
        position,
    )


def test_open_creates_new_session(
    engine,
    position,
    result,
):
    engine.resolve.return_value = result

    session = ReaderSession.open(
        engine=engine,
        position=position,
    )

    assert isinstance(
        session,
        ReaderSession,
    )


# =============================================================
# Current State
# =============================================================


def test_current_position_returns_position(
    engine,
    position,
    result,
):
    engine.resolve.return_value = result

    session = ReaderSession.open(
        engine,
        position,
    )

    assert (
        session.current_position
        is position
    )


def test_current_result_returns_result(
    engine,
    position,
    result,
):
    engine.resolve.return_value = result

    session = ReaderSession.open(
        engine,
        position,
    )

    assert (
        session.current_result
        is result
    )


# =============================================================
# Resolution
# =============================================================


def test_resolve_returns_new_session_with_updated_result(
    engine,
    position,
    result,
):
    first_result = Mock(
        spec=ReaderResult,
    )

    second_result = result

    engine.resolve.side_effect = [
        first_result,
        second_result,
    ]

    session = ReaderSession.open(
        engine,
        position,
    )

    resolved = session.resolve()

    assert resolved is not session

    assert (
        resolved.position
        is session.position
    )

    assert (
        resolved.result
        is second_result
    )

    assert engine.resolve.call_count == 2


def test_resolve_preserves_engine(
    engine,
    position,
    result,
):
    engine.resolve.side_effect = [
        result,
        result,
    ]

    session = ReaderSession.open(
        engine,
        position,
    )

    resolved = session.resolve()

    assert (
        resolved.engine
        is engine
    )


# =============================================================
# Forward Navigation
# =============================================================


def test_move_next_delegates_to_engine(
    engine,
    position,
    next_position,
    result,
    next_result,
):
    engine.resolve.side_effect = [
        result,
        next_result,
    ]

    engine.move_next.return_value = (
        next_position
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    next_session = session.move_next()

    engine.move_next.assert_called_once_with(
        position,
    )

    assert next_session is not None

    assert (
        next_session.position
        is next_position
    )

    assert (
        next_session.result
        is next_result
    )


def test_move_next_returns_new_session(
    engine,
    position,
    next_position,
    result,
    next_result,
):
    engine.resolve.side_effect = [
        result,
        next_result,
    ]

    engine.move_next.return_value = (
        next_position
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    next_session = session.move_next()

    assert next_session is not session


# =============================================================
# Backward Navigation
# =============================================================


def test_move_previous_delegates_to_engine(
    engine,
    position,
    previous_position,
    result,
    previous_result,
):
    engine.resolve.side_effect = [
        result,
        previous_result,
    ]

    engine.move_previous.return_value = (
        previous_position
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    previous_session = (
        session.move_previous()
    )

    engine.move_previous.assert_called_once_with(
        position,
    )

    assert previous_session is not None

    assert (
        previous_session.position
        is previous_position
    )

    assert (
        previous_session.result
        is previous_result
    )


# =============================================================
# Navigation Boundaries
# =============================================================


def test_move_next_returns_none_at_boundary(
    engine,
    position,
    result,
):
    engine.resolve.return_value = result
    engine.move_next.return_value = None

    session = ReaderSession.open(
        engine,
        position,
    )

    assert (
        session.move_next()
        is None
    )


def test_move_previous_returns_none_at_boundary(
    engine,
    position,
    result,
):
    engine.resolve.return_value = result
    engine.move_previous.return_value = None

    session = ReaderSession.open(
        engine,
        position,
    )

    assert (
        session.move_previous()
        is None
    )


# =============================================================
# Session Immutability
# =============================================================


def test_session_is_immutable(
    engine,
    position,
    result,
):
    engine.resolve.return_value = result

    session = ReaderSession.open(
        engine,
        position,
    )

    with pytest.raises(
        Exception,
    ):
        session.position = position


def test_navigation_does_not_mutate_original_session(
    engine,
    position,
    next_position,
    result,
    next_result,
):
    engine.resolve.side_effect = [
        result,
        next_result,
    ]

    engine.move_next.return_value = (
        next_position
    )

    session = ReaderSession.open(
        engine,
        position,
    )

    original_position = (
        session.position
    )

    next_session = session.move_next()

    assert (
        session.position
        is original_position
    )

    assert next_session is not None

    assert (
        next_session.position
        is next_position
    )


# =============================================================
# Convenience
# =============================================================


def test_has_result(
    engine,
    position,
    result,
):
    engine.resolve.return_value = result

    session = ReaderSession.open(
        engine,
        position,
    )

    assert session.has_result is True


def test_succeeded_delegates_to_result(
    engine,
    position,
    result,
):
    result.succeeded = True
    engine.resolve.return_value = result

    session = ReaderSession.open(
        engine,
        position,
    )

    assert session.succeeded is True


# =============================================================
# Display
# =============================================================


def test_display_name(
    engine,
    position,
    result,
):
    engine.resolve.return_value = result

    session = ReaderSession.open(
        engine,
        position,
    )

    assert (
        session.display_name
        == "Reader Session"
    )


def test_display_text_delegates_to_result(
    engine,
    position,
    result,
):
    result.display_text = (
        "Test reader result"
    )

    engine.resolve.return_value = result

    session = ReaderSession.open(
        engine,
        position,
    )

    assert (
        session.display_text
        == "Test reader result"
    )
