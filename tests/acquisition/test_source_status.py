
from SanskritAI.acquisition.models.source_status import SourceStatus


def test_initial_statuses():
    assert SourceStatus.REGISTERED.value == "registered"
    assert SourceStatus.DISCOVERED.value == "discovered"
    assert SourceStatus.PENDING_DOWNLOAD.value == "pending_download"


def test_downloaded_states():
    downloaded_states = (
        SourceStatus.DOWNLOADED,
        SourceStatus.VALIDATING,
        SourceStatus.VALIDATED,
        SourceStatus.NORMALIZING,
        SourceStatus.NORMALIZED,
        SourceStatus.READY_FOR_IMPORT,
        SourceStatus.IMPORTING,
        SourceStatus.IMPORTED,
        SourceStatus.COMPLETED,
        SourceStatus.ARCHIVED,
    )

    for status in downloaded_states:
        assert status.is_downloaded


def test_validated_states():
    validated_states = (
        SourceStatus.VALIDATED,
        SourceStatus.NORMALIZING,
        SourceStatus.NORMALIZED,
        SourceStatus.READY_FOR_IMPORT,
        SourceStatus.IMPORTING,
        SourceStatus.IMPORTED,
        SourceStatus.COMPLETED,
        SourceStatus.ARCHIVED,
    )

    for status in validated_states:
        assert status.is_validated


def test_importable_states():
    importable_states = (
        SourceStatus.READY_FOR_IMPORT,
        SourceStatus.IMPORTING,
        SourceStatus.IMPORTED,
        SourceStatus.COMPLETED,
    )

    for status in importable_states:
        assert status.is_importable


def test_terminal_states():
    terminal_states = (
        SourceStatus.COMPLETED,
        SourceStatus.ARCHIVED,
        SourceStatus.FAILED,
        SourceStatus.SKIPPED,
    )

    for status in terminal_states:
        assert status.is_terminal


def test_failed_state():
    assert SourceStatus.FAILED.has_failed
    assert not SourceStatus.COMPLETED.has_failed


def test_active_states():
    active_states = (
        SourceStatus.DOWNLOADING,
        SourceStatus.VALIDATING,
        SourceStatus.NORMALIZING,
        SourceStatus.IMPORTING,
    )

    for status in active_states:
        assert status.is_active


def test_from_string():
    assert (
        SourceStatus.from_string("registered")
        is SourceStatus.REGISTERED
    )

    assert (
        SourceStatus.from_string(" DOWNLOADED ")
        is SourceStatus.DOWNLOADED
    )


def test_unknown_status():
    assert (
        SourceStatus.from_string("not-a-status")
        is SourceStatus.UNKNOWN
    )


def test_string_representation():
    assert str(SourceStatus.READY_FOR_IMPORT) == "ready_for_import"
