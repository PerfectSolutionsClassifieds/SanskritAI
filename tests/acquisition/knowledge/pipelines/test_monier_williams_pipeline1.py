
from SanskritAI.acquisition.knowledge.connectors.monier_williams_connector import (
    MonierWilliamsConnector,
)
from SanskritAI.acquisition.knowledge.manifests.monier_williams_manifest import (
    MonierWilliamsManifest,
)
from SanskritAI.acquisition.knowledge.parsers.monier_williams_parser import (
    MonierWilliamsParser,
)
from SanskritAI.acquisition.knowledge.pipelines.monier_williams_pipeline import (
    MonierWilliamsPipeline,
)
from SanskritAI.acquisition.knowledge.repositories.canonical_lexical_repository import (
    CanonicalLexicalRepository,
)
from SanskritAI.acquisition.knowledge.transformers.monier_williams_transformer import (
    MonierWilliamsTransformer,
)


# ============================================================
# Construction
# ============================================================

def test_default_pipeline_components():
    pipeline = MonierWilliamsPipeline()

    assert isinstance(
        pipeline.connector,
        MonierWilliamsConnector,
    )

    assert isinstance(
        pipeline.parser,
        MonierWilliamsParser,
    )

    assert isinstance(
        pipeline.transformer,
        MonierWilliamsTransformer,
    )

    assert isinstance(
        pipeline.repository,
        CanonicalLexicalRepository,
    )


# ============================================================
# Validation
# ============================================================

def test_validate_returns_records_unchanged():
    pipeline = MonierWilliamsPipeline()

    records = ["record"]

    assert pipeline.validate(records) is records


# ============================================================
# Manifest
# ============================================================

def test_build_manifest_returns_monier_williams_manifest():
    pipeline = MonierWilliamsPipeline()

    persisted_objects = [
        "entry-1",
        "entry-2",
        "entry-3",
    ]

    manifest = pipeline.build_manifest(
        persisted_objects,
    )

    assert isinstance(
        manifest,
        MonierWilliamsManifest,
    )


def test_build_manifest_sets_record_counts():
    pipeline = MonierWilliamsPipeline()

    persisted_objects = [
        "entry-1",
        "entry-2",
        "entry-3",
    ]

    manifest = pipeline.build_manifest(
        persisted_objects,
    )

    assert manifest.total_records == 3
    assert manifest.imported_records == 3
    assert manifest.skipped_records == 0
    assert manifest.failed_records == 0


def test_build_manifest_sets_source_metadata():
    pipeline = MonierWilliamsPipeline()

    manifest = pipeline.build_manifest(
        ["entry"],
    )

    assert manifest.source_name == "Monier-Williams"
    assert manifest.version == "1.0.0"


def test_build_manifest_handles_empty_collection():
    pipeline = MonierWilliamsPipeline()

    manifest = pipeline.build_manifest([])

    assert manifest.total_records == 0
    assert manifest.imported_records == 0
    assert manifest.skipped_records == 0
    assert manifest.failed_records == 0


# ============================================================
# Pipeline Summary
# ============================================================

def test_pipeline_summary():
    pipeline = MonierWilliamsPipeline()

    summary = pipeline.summary()

    assert summary == {
        "pipeline": "MonierWilliamsPipeline",
        "connector": "MonierWilliamsConnector",
        "parser": "MonierWilliamsParser",
        "transformer": "MonierWilliamsTransformer",
        "repository": "CanonicalLexicalRepository",
    }


# ============================================================
# String Representation
# ============================================================

def test_string_representation():
    pipeline = MonierWilliamsPipeline()

    text = str(pipeline)

    assert text.startswith(
        "MonierWilliamsPipeline("
    )

    assert "MonierWilliamsConnector" in text
