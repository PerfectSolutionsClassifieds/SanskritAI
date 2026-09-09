from __future__ import annotations

from SanskritAI.acquisition.acquirers.source_acquirer import (
    SourceAcquirer,
)
from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)
from SanskritAI.acquisition.models.acquisition_result import (
    AcquisitionResult,
)
from SanskritAI.acquisition.pipelines.acquisition_pipeline import (
    AcquisitionPipeline,
)
from SanskritAI.acquisition.services.acquisition_service import (
    AcquisitionService,
)
from SanskritAI.acquisition.services.default_acquisition_service import (
    DefaultAcquisitionService,
)
from SanskritAI.acquisition.lexical.monier_williams.monier_williams_acquisition_service import (
    MonierWilliamsAcquisitionService,
)
from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source import (
    MonierWilliamsSource,
)


# ----------------------------------------------------------------------
# Structural separation
# ----------------------------------------------------------------------

def test_monier_williams_source_is_not_generic_source_acquirer():
    assert not issubclass(
        MonierWilliamsSource,
        SourceAcquirer,
    )


def test_monier_williams_acquisition_service_is_not_generic_service():
    assert not issubclass(
        MonierWilliamsAcquisitionService,
        AcquisitionService,
    )


def test_monier_williams_service_is_not_generic_pipeline():
    assert not issubclass(
        MonierWilliamsAcquisitionService,
        AcquisitionPipeline,
    )


def test_monier_williams_service_does_not_use_generic_manifest_as_primary_input():
    """
    MW acquisition is source-oriented and therefore must not accidentally
    become a generic AcquisitionManifest service.

    The test intentionally checks the constructor/dataclass fields rather
    than runtime implementation details.
    """

    annotations = getattr(
        MonierWilliamsAcquisitionService,
        "__annotations__",
        {},
    )

    assert "source" in annotations


# ----------------------------------------------------------------------
# Generic architecture remains independently usable
# ----------------------------------------------------------------------

class FakeGenericAcquirer(SourceAcquirer):
    def __init__(self) -> None:
        self.calls: list[AcquisitionManifest] = []

    def acquire(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:
        self.calls.append(manifest)

        return AcquisitionResult(
            source=manifest.source,
            success=True,
        )


def test_generic_acquisition_stack_remains_independent():
    from SanskritAI.acquisition.models.corpus_source import CorpusSource
    from SanskritAI.acquisition.models.source_format import SourceFormat

    source = CorpusSource(
        source_id="generic-test-source",
        name="Generic Test Source",
        source_type="corpus",
        source_format=SourceFormat.TEXT,
    )

    manifest = AcquisitionManifest(
        manifest_id="generic-test-manifest",
        source=source,
    )

    acquirer = FakeGenericAcquirer()
    pipeline = AcquisitionPipeline(acquirer=acquirer)
    service = DefaultAcquisitionService(pipeline=pipeline)

    result = service.acquire(manifest)

    assert result.success is True
    assert result.source is source
    assert acquirer.calls == [manifest]

    
