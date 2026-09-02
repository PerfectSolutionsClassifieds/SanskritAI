
from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.acquisition.knowledge.connectors.monier_williams_connector import (
    MonierWilliamsConnector,
)
from SanskritAI.acquisition.knowledge.monier_williams_manifest import (
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


def test_build_manifest_sets_monier_williams_identity():
    pipeline = MonierWilliamsPipeline()

    manifest = pipeline.build_manifest(
        ["entry"],
    )

    assert manifest.identifier == "MW"

    assert (
        manifest.resource_name
        == "Monier-Williams Sanskrit Dictionary"
    )

    assert manifest.short_name == "MW"


def test_build_manifest_sets_resource_version():
    pipeline = MonierWilliamsPipeline()

    manifest = pipeline.build_manifest(
        ["entry"],
    )

    assert manifest.version == "1.0.0"


def test_build_manifest_sets_resource_metadata():
    pipeline = MonierWilliamsPipeline()

    manifest = pipeline.build_manifest(
        ["entry"],
    )

    assert manifest.provider == "Monier-Williams"

    assert manifest.language == "sa"

    assert manifest.script == "Devanagari"

    assert manifest.transliteration_scheme == "IAST"


def test_build_manifest_declares_pipeline_components():
    pipeline = MonierWilliamsPipeline()

    manifest = pipeline.build_manifest(
        ["entry"],
    )

    assert (
        manifest.connector_name
        == "MonierWilliamsConnector"
    )

    assert (
        manifest.parser_name
        == "MonierWilliamsParser"
    )

    assert (
        manifest.transformer_name
        == "MonierWilliamsTransformer"
    )


def test_build_manifest_handles_empty_collection():
    pipeline = MonierWilliamsPipeline()

    manifest = pipeline.build_manifest([])

    assert isinstance(
        manifest,
        MonierWilliamsManifest,
    )

    assert manifest.identifier == "MW"

    assert manifest.version == "1.0.0"


# ============================================================
# Manifest Immutability
# ============================================================


def test_build_manifest_returns_frozen_manifest():
    pipeline = MonierWilliamsPipeline()

    manifest = pipeline.build_manifest(
        ["entry"],
    )

    with pytest.raises(FrozenInstanceError):
        manifest.version = "2.0"


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

    assert (
        "MonierWilliamsConnector"
        in text
    )


    
