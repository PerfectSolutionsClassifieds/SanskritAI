from __future__ import annotations

"""
SanskritAI
==========

Pipeline Factory

Factory responsible for constructing reusable Pipeline
instances from the canonical PipelineRegistry.

The PipelineFactory is intentionally domain-independent.
It acts as the bridge between

    PipelineBuilder
            ↓
    PipelineRegistry
            ↓
    Pipeline

and will later construct

    • DefaultDerivationPipeline
    • DefaultSemanticPipeline
    • DefaultVakyaPipeline
    • DefaultChandasPipeline
    • DefaultAlankaraPipeline
    • DefaultKnowledgeGraphPipeline
    • UniversalKernelPipeline

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.core.pipeline.pipeline import Pipeline
from SanskritAI.core.pipeline.pipeline_builder import PipelineBuilder
from SanskritAI.core.pipeline.pipeline_registry import (
    PipelineRegistry,
)


@dataclass(slots=True)
class PipelineFactory(Displayable):
    """
    Factory for constructing reusable Pipeline objects.
    """

    registry: PipelineRegistry = field(
        default_factory=PipelineRegistry,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Pipeline Factory"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Constructs reusable Pipeline instances "
            "from the canonical PipelineRegistry."
        )

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        pipeline: Pipeline,
        *,
        overwrite: bool = False,
    ) -> "PipelineFactory":
        """
        Registers a Pipeline.

        Returns the factory for fluent chaining.
        """
        self.registry.register(
            pipeline,
            overwrite=overwrite,
        )
        return self

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Pipeline | None:
        """
        Returns a registered Pipeline.
        """
        return self.registry.get(name)

    def require(
        self,
        name: str,
    ) -> Pipeline:
        """
        Returns a Pipeline or raises KeyError.
        """
        return self.registry.require(name)

    # ---------------------------------------------------------
    # Creation
    # ---------------------------------------------------------

    def create(
        self,
        name: str,
    ) -> Pipeline:
        """
        Creates (returns) a registered Pipeline.

        At the Core level, pipelines are immutable, so this
        simply returns the registered instance.
        """
        return self.require(name)

    def create_from_builder(
        self,
        builder: PipelineBuilder,
        *,
        register: bool = False,
        overwrite: bool = False,
    ) -> Pipeline:
        """
        Builds a Pipeline from a PipelineBuilder.

        Optionally registers the resulting pipeline.
        """

        pipeline = builder.build()

        if register:
            self.register(
                pipeline,
                overwrite=overwrite,
            )

        return pipeline

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def pipeline_count(self) -> int:
        return self.registry.pipeline_count

    @property
    def pipelines(
        self,
    ) -> tuple[Pipeline, ...]:
        return self.registry.pipelines

    @property
    def names(
        self,
    ) -> tuple[str, ...]:
        return self.registry.names

    # ---------------------------------------------------------

    def __contains__(
        self,
        name: str,
    ) -> bool:
        return name in self.registry

    def __len__(
        self,
    ) -> int:
        return len(self.registry)

    def __iter__(
        self,
    ):
        return iter(self.registry)

    def __str__(self) -> str:
        return (
            f"{self.display_name}"
            f" ({self.pipeline_count} pipelines)"
        )
