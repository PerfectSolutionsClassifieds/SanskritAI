
from SanskritAI.acquisition.lexical.monier_williams import (
    MonierWilliamsAcquisitionService,
    MonierWilliamsSource,
    MonierWilliamsSourcePipeline,
    MonierWilliamsSourceRecord,
)


class StubSource(MonierWilliamsSource):
    @property
    def identifier(self):
        return "test:mw"

    @property
    def source_name(self):
        return "Test MW"

    def read(self):
        return (
            "<L>1\n"
            "<k1>rAma\n"
            "<h>m.\n"
            "<e>pleasing, beautiful\n"
            "<LEND>\n"
        )


def test_pipeline_acquires_and_parses():
    service = MonierWilliamsAcquisitionService(
        StubSource()
    )

    pipeline = MonierWilliamsSourcePipeline(
        service
    )

    records = pipeline.parse()

    assert len(records) == 1

    record = records[0]

    assert isinstance(
        record,
        MonierWilliamsSourceRecord,
    )

    assert record.sequence == 1
    assert record.headword == "rAma"
    assert record.get("h") == "m."
    assert record.get("e") == "pleasing, beautiful"


def test_pipeline_returns_source_records_only():
    service = MonierWilliamsAcquisitionService(
        StubSource()
    )

    pipeline = MonierWilliamsSourcePipeline(
        service
    )

    records = pipeline.records()

    assert isinstance(records, tuple)

    assert all(
        isinstance(
            record,
            MonierWilliamsSourceRecord,
        )
        for record in records
    )


def test_pipeline_preserves_native_mw_raw_text():
    service = MonierWilliamsAcquisitionService(
        StubSource()
    )

    pipeline = MonierWilliamsSourcePipeline(
        service
    )

    record = pipeline.records()[0]

    assert "<L>1" in record.raw_text
    assert "<k1>rAma" in record.raw_text
    assert "<e>pleasing, beautiful" in record.raw_text
    assert "<LEND>" in record.raw_text
