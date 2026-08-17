from __future__ import annotations

from unittest.mock import Mock

from SanskritAI.domain.morphology.default_morphological_resolution_kernel import (
    DefaultMorphologicalResolutionKernel,
)

from SanskritAI.domain.morphology.morphological_repository import (
    MorphologicalRepository,
)

from SanskritAI.domain.morphology.morphological_resolution_context import (
    MorphologicalResolutionContext,
)

from SanskritAI.domain.morphology.morphological_resolution_result import (
    MorphologicalResolutionResult,
)

from SanskritAI.domain.morphology.morphological_resolution_strategy import (
    MorphologicalResolutionStrategy,
)


class TestDefaultMorphologicalResolutionKernel:

    def test_can_be_created_with_repository(self):
        repository = Mock(spec=MorphologicalRepository)

        kernel = DefaultMorphologicalResolutionKernel(
            repository=repository,
        )

        assert kernel is not None
        assert kernel.repository is repository

    def test_default_strategy_is_created(self):
        repository = Mock(spec=MorphologicalRepository)

        kernel = DefaultMorphologicalResolutionKernel(
            repository=repository,
        )

        assert isinstance(
            kernel.strategy,
            MorphologicalResolutionStrategy,
        )

    def test_custom_strategy_is_preserved(self):
        repository = Mock(spec=MorphologicalRepository)
        strategy = Mock(
            spec=MorphologicalResolutionStrategy,
        )

        kernel = DefaultMorphologicalResolutionKernel(
            repository=repository,
            strategy=strategy,
        )

        assert kernel.strategy is strategy

    def test_resolution_strategy_returns_strategy(self):
        repository = Mock(spec=MorphologicalRepository)
        strategy = Mock(
            spec=MorphologicalResolutionStrategy,
        )

        kernel = DefaultMorphologicalResolutionKernel(
            repository=repository,
            strategy=strategy,
        )

        assert kernel.resolution_strategy is strategy

    def test_kernel_exposes_generic_resolution_kernel(self):
        repository = Mock(spec=MorphologicalRepository)

        kernel = DefaultMorphologicalResolutionKernel(
            repository=repository,
        )

        assert kernel.kernel is not None

    def test_resolve_delegates_to_strategy(self):
        repository = Mock(spec=MorphologicalRepository)

        strategy = Mock(
            spec=MorphologicalResolutionStrategy,
        )

        context = Mock(
            spec=MorphologicalResolutionContext,
        )

        expected = Mock(
            spec=MorphologicalResolutionResult,
        )

        strategy.resolve.return_value = expected

        kernel = DefaultMorphologicalResolutionKernel(
            repository=repository,
            strategy=strategy,
        )

        result = kernel.resolve(context)

        assert result is expected

        strategy.resolve.assert_called_once_with(
            context,
        )

    def test_call_delegates_to_resolve(self):
        repository = Mock(spec=MorphologicalRepository)

        strategy = Mock(
            spec=MorphologicalResolutionStrategy,
        )

        context = Mock(
            spec=MorphologicalResolutionContext,
        )

        expected = Mock(
            spec=MorphologicalResolutionResult,
        )

        strategy.resolve.return_value = expected

        kernel = DefaultMorphologicalResolutionKernel(
            repository=repository,
            strategy=strategy,
        )

        result = kernel(context)

        assert result is expected

    def test_display_contract(self):
        repository = Mock(spec=MorphologicalRepository)

        kernel = DefaultMorphologicalResolutionKernel(
            repository=repository,
        )

        assert (
            kernel.display_name
            == "Default Morphological Resolution Kernel"
        )

        assert (
            kernel.display_text
            == kernel.display_name
        )

        assert kernel.display_description

    def test_string_representation(self):
        repository = Mock(spec=MorphologicalRepository)

        kernel = DefaultMorphologicalResolutionKernel(
            repository=repository,
        )

        assert str(kernel) == kernel.display_text
