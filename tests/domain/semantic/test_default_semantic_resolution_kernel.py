from __future__ import annotations

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.semantic.default_semantic_resolution_kernel import (
    DefaultSemanticResolutionKernel,
)

from SanskritAI.domain.semantic.semantic_context import (
    SemanticContext,
)


class StubSemanticRepository:

    count = 0


def make_context():

    return ResolutionContext(
        identifier="semantic-kernel-test",
        subject="धर्मः",
        source="unit-test",
        language="Sanskrit",
        script="Devanagari",
        metadata={},
    )


def test_default_kernel_can_be_constructed():

    repository = StubSemanticRepository()

    kernel = DefaultSemanticResolutionKernel(
        repository=repository,
    )

    assert kernel.repository is repository


def test_default_kernel_exposes_generic_kernel():

    repository = StubSemanticRepository()

    kernel = DefaultSemanticResolutionKernel(
        repository=repository,
    )

    assert kernel.kernel is not None


def test_default_kernel_builds_semantic_context():

    repository = StubSemanticRepository()

    kernel = DefaultSemanticResolutionKernel(
        repository=repository,
    )

    semantic_context = kernel.build_context(
        make_context(),
    )

    assert isinstance(
        semantic_context,
        SemanticContext,
    )

    assert semantic_context.identifier == (
        "semantic-kernel-test"
    )

    assert semantic_context.subject == "धर्मः"
    assert semantic_context.language == "Sanskrit"
    assert semantic_context.script == "Devanagari"


def test_default_kernel_preserves_metadata():

    repository = StubSemanticRepository()

    kernel = DefaultSemanticResolutionKernel(
        repository=repository,
    )

    context = ResolutionContext(
        identifier="metadata-test",
        subject="अर्थः",
        source="unit-test",
        language="Sanskrit",
        script="Devanagari",
        metadata={
            "allow_multiple_analyses": False,
            "enable_recursive_analysis": False,
        },
    )

    semantic_context = kernel.build_context(
        context,
    )

    assert semantic_context.allow_multiple_analyses is False
    assert semantic_context.enable_recursive_analysis is False
