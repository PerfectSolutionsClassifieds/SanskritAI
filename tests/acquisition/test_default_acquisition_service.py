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

from SanskritAI.acquisition.models.corpus_source import (
    CorpusSource,
)

from SanskritAI.acquisition.models.source_format import (
    SourceFormat,
)

from SanskritAI.acquisition.pipelines.acquisition_pipeline import (
    AcquisitionPipeline,
)

from SanskritAI.acquisition.services.default_acquisition_service import (
    DefaultAcquisitionService,
)


class FakeSourceAcquirer(SourceAcquirer):

    def __init__(self):
        self.calls = []

    def acquire(
        self,
        manifest: AcquisitionManifest,
    ) -> AcquisitionResult:

        self.calls.append(manifest)

        return AcquisitionResult(
            source=manifest.source,
            success=True,
            message="fake acquisition",
        )


def make_source() -> CorpusSource:
    return CorpusSource(
        source_id="test-source",
        name="Test Source",
        source_type="corpus",
        source_format=SourceFormat.TEXT,
    )


def make_manifest() -> AcquisitionManifest:
    return AcquisitionManifest(
        manifest_id="test-manifest",
        source=make_source(),
    )


def make_service():
    acquirer = FakeSourceAcquirer()

    pipeline = AcquisitionPipeline(
        acquirer=acquirer,
    )

    service = DefaultAcquisitionService(
        pipeline=pipeline,
    )

    return service, acquirer


def test_default_service_delegates_to_pipeline():

    service, acquirer = make_service()

    manifest = make_manifest()

    result = service.acquire(manifest)

    assert result.success is True
    assert result.source is manifest.source
    assert acquirer.calls == [manifest]


def test_default_service_run_alias():

    service, acquirer = make_service()

    manifest = make_manifest()

    result = service.run(manifest)

    assert result.success is True
    assert acquirer.calls == [manifest]


def test_default_service_display():

    service, _ = make_service()

    assert service.display_name == "Default Acquisition Service"
    assert service.display_text == "Default Acquisition Service"
    assert "acquisition" in service.display_description.lower()


def test_default_service_is_frozen():

    service, _ = make_service()

    try:
        service.pipeline = service.pipeline
    except Exception:
        pass
    else:
        raise AssertionError(
            "DefaultAcquisitionService should be immutable"
        )
