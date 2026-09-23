from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.acquisition.lexical.monier_williams import (
    DelimitedMonierWilliamsParser,
    MonierWilliamsAcquisitionService,
    MonierWilliamsSource,
)


@dataclass
class StubSource(MonierWilliamsSource):
    content: str

    def read(self) -> str:
        return self.content


def test_acquisition_service_reads_and_parses_source():
    source = StubSource(
        "headword\tdefinition\n"
        "देव\tgod\n"
        "राम\tRama\n"
    )

    parser = DelimitedMonierWilliamsParser()

    service = MonierWilliamsAcquisitionService(
        source=source,
        parser=parser,
    )

    records = service.acquire()

    assert len(records) == 2
    assert records[0].headword == "देव"
    assert records[1].headword == "राम"


def test_acquisition_service_count():
    source = StubSource(
        "headword\tdefinition\n"
        "देव\tgod\n"
    )

    service = MonierWilliamsAcquisitionService(
        source=source,
        parser=DelimitedMonierWilliamsParser(),
    )

    assert service.count() == 1


def test_acquisition_service_preserves_source_boundary():
    source = StubSource(
        "headword\tdefinition\n"
        "देव\tgod\n"
    )

    service = MonierWilliamsAcquisitionService(
        source=source,
        parser=DelimitedMonierWilliamsParser(),
    )

    records = service.acquire()

    assert records[0].source == "monier-williams"
