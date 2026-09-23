
from pathlib import Path

import pytest

from SanskritAI.acquisition.lexical.monier_williams import (
    LocalMonierWilliamsSourceAcquirer,
    MonierWilliamsAcquisitionService,
    MonierWilliamsSource,
    MonierWilliamsSourceAcquirer,
)


# ---------------------------------------------------------------------------
# Test source doubles
# ---------------------------------------------------------------------------


class StubSource(MonierWilliamsSource):
    """Minimal source implementation for service-boundary tests."""

    def __init__(self, text: str):
        self._text = text

    def read(self) -> str:
        return self._text


class StubParser:
    """Minimal parser used only to verify service delegation."""

    def __init__(self):
        self.received = None

    def parse(self, text: str):
        self.received = text
        return tuple(text.splitlines())


# ---------------------------------------------------------------------------
# Service boundary
# ---------------------------------------------------------------------------


def test_acquisition_service_remains_source_oriented():
    source = StubSource("रामः\nगच्छति")

    service = MonierWilliamsAcquisitionService(
        source=source,
    )

    assert service.source is source


def test_acquisition_service_does_not_require_source_acquirer():
    source = StubSource("रामः\nगच्छति")

    service = MonierWilliamsAcquisitionService(
        source=source,
    )

    assert service.read() == "रामः\nगच्छति"


def test_acquisition_service_can_still_delegate_to_parser():
    source = StubSource("रामः\nगच्छति")
    parser = StubParser()

    service = MonierWilliamsAcquisitionService(
        source=source,
        parser=parser,
    )

    result = service.acquire()

    assert parser.received == "रामः\nगच्छति"
    assert result == ("रामः", "गच्छति")


# ---------------------------------------------------------------------------
# Source-acquirer boundary
# ---------------------------------------------------------------------------


def test_local_source_acquirer_is_an_independent_acquisition_mechanism(
    tmp_path: Path,
):
    source_file = tmp_path / "mw.txt"
    source_file.write_text(
        "रामः\nगच्छति\n",
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(source_file)

    assert isinstance(acquirer, MonierWilliamsSourceAcquirer)
    assert acquirer.acquire() == "रामः\nगच्छति\n"


def test_local_source_acquirer_does_not_require_acquisition_service(
    tmp_path: Path,
):
    source_file = tmp_path / "mw.txt"
    source_file.write_text(
        "रामः\nगच्छति\n",
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(source_file)

    assert acquirer.acquire() == "रामः\ngच्छति\n"


def test_source_acquirer_output_can_feed_parser_directly(
    tmp_path: Path,
):
    source_file = tmp_path / "mw.txt"
    source_file.write_text(
        "रामः\nगच्छति\n",
        encoding="utf-8",
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(source_file)

    raw_text = acquirer.acquire()

    parser = StubParser()
    result = parser.parse(raw_text)

    assert parser.received == raw_text
    assert result == ("रामः", "गच्छति")


# ---------------------------------------------------------------------------
# Explicit architectural non-dependency
# ---------------------------------------------------------------------------


def test_acquisition_service_does_not_depend_on_source_acquirer_type():
    source = StubSource("रामः")

    service = MonierWilliamsAcquisitionService(
        source=source,
    )

    assert not isinstance(
        service.source,
        MonierWilliamsSourceAcquirer,
    )


def test_source_and_source_acquirer_are_distinct_boundaries():
    source = StubSource("रामः")

    assert isinstance(source, MonierWilliamsSource)
    assert not isinstance(source, MonierWilliamsSourceAcquirer)

    service = MonierWilliamsAcquisitionService(
        source=source,
    )

    assert service.source is source


def test_local_acquirer_and_service_can_coexist_without_being_coupled(
    tmp_path: Path,
):
    source_file = tmp_path / "mw.txt"
    source_file.write_text(
        "रामः\nगच्छति\n",
        encoding="utf-8",
    )

    source = StubSource("रामः\nगच्छति")
    service = MonierWilliamsAcquisitionService(
        source=source,
    )

    acquirer = LocalMonierWilliamsSourceAcquirer(source_file)

    assert service.read() == "रामः\nगच्छति"
    assert acquirer.acquire() == "रामः\nगच्छति\n"

    
