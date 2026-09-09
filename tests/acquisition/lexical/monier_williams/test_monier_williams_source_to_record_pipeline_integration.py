
from SanskritAI.acquisition.lexical.monier_williams.monier_williams_acquisition_service import (
    MonierWilliamsAcquisitionService,
)

from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source import (
    MonierWilliamsSource,
)

from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source_pipeline import (
    MonierWilliamsSourcePipeline,
)

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


MW_SAMPLE = """\
<L>1
<k1>rAma
<k2>1
<h>m.
<e>pleasing, beautiful
<LEND>
<L>2
<k1>hari
<h>m.
<e>yellow, tawny
<LEND>
"""


class StubSource(MonierWilliamsSource):

    def __init__(self, text: str):
        self.text = text

    def read(self) -> str:
        return self.text


def test_pipeline_normalizes_source_records_to_adapter_records():

    service = MonierWilliamsAcquisitionService(
        source=StubSource(MW_SAMPLE)
    )

    pipeline = MonierWilliamsSourcePipeline(
        service=service
    )

    source_records = pipeline.records()

    assert len(source_records) == 2

    normalized = pipeline.normalized_records()

    assert len(normalized) == 2

    assert all(
        isinstance(
            record,
            MonierWilliamsRecord,
        )
        for record in normalized
    )

    assert normalized[0].headword == "rAma"
    assert normalized[0].definition == (
        "pleasing, beautiful"
    )
    assert normalized[0].grammatical_label == "m."

    assert normalized[1].headword == "hari"
    assert normalized[1].definition == (
        "yellow, tawny"
    )
    
