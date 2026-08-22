
from SanskritAI.acquisition.lexical.monier_williams import (
    MonierWilliamsAcquisitionService,
    MonierWilliamsSource,
)


class StubSource(MonierWilliamsSource):

    def __init__(self, text):
        self.text = text
        self.read_count = 0

    @property
    def identifier(self):
        return "test:mw"

    @property
    def source_name(self):
        return "Test MW Source"

    def read(self):
        self.read_count += 1
        return self.text


def test_acquisition_service_reads_source():
    source = StubSource("mw source")

    service = MonierWilliamsAcquisitionService(source)

    result = service.acquire()

    assert result.text == "mw source"
    assert result.source_identifier == "test:mw"
    assert result.source_name == "Test MW Source"


def test_acquisition_service_returns_counts():
    source = StubSource(
        "first\n"
        "second\n"
    )

    result = MonierWilliamsAcquisitionService(
        source
    ).acquire()

    assert result.character_count == len(
        "first\nsecond\n"
    )
    assert result.line_count == 2


def test_acquisition_service_read_is_convenience_method():
    source = StubSource("mw")

    service = MonierWilliamsAcquisitionService(source)

    assert service.read() == "mw"


def test_source_is_not_replaced():
    source = StubSource("mw")

    service = MonierWilliamsAcquisitionService(source)

    assert service.source is source
