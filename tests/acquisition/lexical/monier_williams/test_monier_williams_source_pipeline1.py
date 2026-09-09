
from SanskritAI.acquisition.lexical.monier_williams import (
    MonierWilliamsAcquisitionService,
    MonierWilliamsSource,
    MonierWilliamsSourcePipeline,
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
            "<e>pleasing\n"
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
    assert records[0].headword == "rAma"
    assert records[0].get("e") == "pleasing"
