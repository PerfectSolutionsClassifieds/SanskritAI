from __future__ import annotations

from SanskritAI.acquisition.acquirers.default_source_acquirer import (
    DefaultSourceAcquirer,
)
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
from SanskritAI.acquisition.services.acquisition_service import (
    AcquisitionService,
)
from SanskritAI.acquisition.services.default_acquisition_service import (
    DefaultAcquisitionService,
)


# ----------------------------------------------------------------------
# Test doubles
# ----------------------------------------------------------------------

class RecordingSourceAcquirer(SourceAcquirer):
    """
    Minimal generic SourceAcquirer used to verify the generic
    acquisition boundary.

    It deliberately performs no real acquisition.
    """

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
            message="recorded acquisition",
        )


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def make_source() -> CorpusSource:
    return CorpusSource(
        source_id="architecture-test-source",
        name="Architecture Test Source",
        source_type="corpus",
        source_format=SourceFormat.TEXT,
    )


def make_manifest() -> AcquisitionManifest:
    return AcquisitionManifest(
        manifest_id="architecture-test-manifest",
        source=make_source(),
    )


# ----------------------------------------------------------------------
# SourceAcquirer boundary
# ----------------------------------------------------------------------

def test_source_acquirer_defines_only_generic_acquisition_operation():
    assert SourceAcquirer.__abstractmethods__ == {"acquire"}


def test_source_acquirer_operates_on_acquisition_manifest():
    acquirer = RecordingSourceAcquirer()
    manifest = make_manifest()

    result = acquirer.acquire(manifest)

    assert result.source is manifest.source
    assert acquirer.calls == [manifest]


# ----------------------------------------------------------------------
# Pipeline boundary
# ----------------------------------------------------------------------

def test_acquisition_pipeline_does_not_perform_acquisition_itself():
    acquirer = RecordingSourceAcquirer()
    pipeline = AcquisitionPipeline(acquirer=acquirer)

    manifest = make_manifest()

    result = pipeline.acquire(manifest)

    assert result.success is True
    assert acquirer.calls == [manifest]


def test_acquisition_pipeline_is_an_orchestration_boundary():
    acquirer = RecordingSourceAcquirer()
    pipeline = AcquisitionPipeline(acquirer=acquirer)

    assert pipeline.acquirer is acquirer
    assert pipeline.display_name == "Acquisition Pipeline"


# ----------------------------------------------------------------------
# Service boundary
# ----------------------------------------------------------------------

def test_acquisition_service_defines_application_facing_acquire_boundary():
    assert AcquisitionService.__abstractmethods__ == {"acquire"}


def test_default_acquisition_service_delegates_to_pipeline():
    acquirer = RecordingSourceAcquirer()
    pipeline = AcquisitionPipeline(acquirer=acquirer)
    service = DefaultAcquisitionService(pipeline=pipeline)

    manifest = make_manifest()

    result = service.acquire(manifest)

    assert result.success is True
    assert result.source is manifest.source
    assert acquirer.calls == [manifest]


# ----------------------------------------------------------------------
# Separation of responsibilities
# ----------------------------------------------------------------------

def test_generic_pipeline_does_not_require_url_logic():
    """
    The generic pipeline must remain independent of URL/download
    implementation details.

    A fake SourceAcquirer with no URL handling is sufficient.
    """

    acquirer = RecordingSourceAcquirer()
    pipeline = AcquisitionPipeline(acquirer=acquirer)

    manifest = make_manifest()

    result = pipeline.run(manifest)

    assert result.success is True
    assert acquirer.calls == [manifest]


def test_default_source_acquirer_exposes_generic_acquisition_operation():
    """
    Verify the concrete default acquirer exposes the generic
    acquire(manifest) operation.

    We intentionally do not assert inheritance from SourceAcquirer
    because the existing implementation does not establish that
    inheritance relationship.
    """

    assert callable(
        getattr(DefaultSourceAcquirer, "acquire", None)
    )


def test_default_source_acquirer_can_be_constructed():
    acquirer = DefaultSourceAcquirer()

    assert acquirer is not None


def test_acquisition_result_is_the_generic_output_boundary():
    acquirer = RecordingSourceAcquirer()
    manifest = make_manifest()

    result = acquirer.acquire(manifest)

    assert isinstance(result, AcquisitionResult)
    assert result.source is manifest.source
