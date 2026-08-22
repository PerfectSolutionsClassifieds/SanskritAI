from __future__ import annotations

from pathlib import Path

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


def test_pipeline_delegates_to_acquirer():

    acquirer = FakeSourceAcquirer()
    pipeline = AcquisitionPipeline(
        acquirer=acquirer,
    )

    manifest = make_manifest()

    result = pipeline.acquire(manifest)

    assert result.success is True
    assert result.source is manifest.source
    assert acquirer.calls == [manifest]


def test_pipeline_run_is_alias_for_acquire():

    acquirer = FakeSourceAcquirer()
    pipeline = AcquisitionPipeline(
        acquirer=acquirer,
    )

    manifest = make_manifest()

    result = pipeline.run(manifest)

    assert result.success is True
    assert acquirer.calls == [manifest]


def test_pipeline_display():

    acquirer = FakeSourceAcquirer()
    pipeline = AcquisitionPipeline(
        acquirer=acquirer,
    )

    assert pipeline.display_name == "Acquisition Pipeline"
    assert pipeline.display_text == "Acquisition Pipeline"
    assert "acquisition" in pipeline.display_description.lower()


def test_pipeline_is_frozen():

    acquirer = FakeSourceAcquirer()
    pipeline = AcquisitionPipeline(
        acquirer=acquirer,
    )

    try:
        pipeline.acquirer = acquirer
    except Exception:
        pass
    else:
        raise AssertionError(
            "AcquisitionPipeline should be immutable"
        )
