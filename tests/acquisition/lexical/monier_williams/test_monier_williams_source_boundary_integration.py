
from SanskritAI.acquisition.lexical.monier_williams import (
    MonierWilliamsAcquisitionService,
    MonierWilliamsSource,
    MonierWilliamsSourceParser,
    MonierWilliamsSourcePipeline,
    MonierWilliamsSourceRecord,
)


MW_SOURCE = """\
<L>1
<k1>rAma
<h>m.
<e>pleasing, beautiful
<LEND>
<L>2
<k1>hari
<h>m.
<e>yellow, tawny
<LEND>
"""


class BoundaryStubSource(MonierWilliamsSource):

    @property
    def identifier(self):
        return "test:mw:boundary"

    @property
    def source_name(self):
        return "Boundary Test MW"

    def read(self):
        return MW_SOURCE


def test_raw_source_flows_through_complete_boundary():
    source = BoundaryStubSource()

    service = MonierWilliamsAcquisitionService(source)

    parser = MonierWilliamsSourceParser()

    pipeline = MonierWilliamsSourcePipeline(
        service=service,
        parser=parser,
    )

    records = pipeline.records()

    assert isinstance(records, tuple)
    assert len(records) == 2

    assert all(
        isinstance(record, MonierWilliamsSourceRecord)
        for record in records
    )

    assert records[0].sequence == 1
    assert records[0].headword == "rAma"
    assert records[0].get("h") == "m."
    assert records[0].get("e") == "pleasing, beautiful"

    assert records[1].sequence == 2
    assert records[1].headword == "hari"
    assert records[1].get("e") == "yellow, tawny"


def test_source_boundary_preserves_raw_mw_record_text():
    service = MonierWilliamsAcquisitionService(
        BoundaryStubSource()
    )

    pipeline = MonierWilliamsSourcePipeline(
        service=service,
        parser=MonierWilliamsSourceParser(),
    )

    records = pipeline.records()

    assert "<L>1" in records[0].raw_text
    assert "<k1>rAma" in records[0].raw_text
    assert "<LEND>" in records[0].raw_text

    assert "<L>2" in records[1].raw_text
    assert "<k1>hari" in records[1].raw_text
    assert "<LEND>" in records[1].raw_text


def test_pipeline_uses_injected_parser_as_single_parser_authority():
    service = MonierWilliamsAcquisitionService(
        BoundaryStubSource()
    )

    parser = MonierWilliamsSourceParser()

    pipeline = MonierWilliamsSourcePipeline(
        service=service,
        parser=parser,
    )

    records = pipeline.parse()

    assert isinstance(records, tuple)
    assert records[0].headword == "rAma"
    assert records[1].headword == "hari"
