from __future__ import annotations

"""
SanskritAI
==========

Pipeline Builder

Provides a fluent builder for constructing immutable
Pipeline instances.

The builder is intentionally generic and independent of any
particular SanskritAI kernel.  It may therefore be used for

    • Derivation Pipeline
    • Semantic Pipeline
    • Vakya Pipeline
    • Chandas Pipeline
    • Alankara Pipeline
    • Knowledge Graph Pipeline
    • Future kernels

Example
-------

pipeline = (
    PipelineBuilder()
        .named("Derivation Pipeline")
        .add_step(step1)
        .add_step(step2)
        .build()
)

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.pipeline.pipeline import Pipeline
from SanskritAI.core.pipeline.pipeline_step import PipelineStep


@dataclass(slots=True)
class PipelineBuilder(Displayable):
    """
    Fluent builder for immutable Pipeline objects.
    """

    _name: str = "Pipeline"

    _steps: list[PipelineStep] = field(
        default_factory=list,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Pipeline Builder"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Fluent builder for constructing "
            "Pipeline instances."
        )

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def named(
        self,
        name: str,
    ) -> "PipelineBuilder":
        """
        Sets the pipeline name.
        """
        self._name = name
        return self

    def add_step(
        self,
        step: PipelineStep,
    ) -> "PipelineBuilder":
        """
        Adds a pipeline step.

        Duplicate identifiers are ignored.
        """
        if not any(
            existing.identifier == step.identifier
            for existing in self._steps
        ):
            self._steps.append(step)

        return self

    def add_steps(
        self,
        *steps: PipelineStep,
    ) -> "PipelineBuilder":
        """
        Adds multiple pipeline steps.
        """
        for step in steps:
            self.add_step(step)

        return self

    def clear(
        self,
    ) -> "PipelineBuilder":
        """
        Removes all configured steps.
        """
        self._steps.clear()
        return self

    # ---------------------------------------------------------
    # Inspection
    # ---------------------------------------------------------

    @property
    def step_count(self) -> int:
        return len(self._steps)

    @property
    def is_empty(self) -> bool:
        return self.step_count == 0

    @property
    def ordered_steps(
        self,
    ) -> tuple[PipelineStep, ...]:
        """
        Returns steps ordered by priority.
        """
        return tuple(
            sorted(
                self._steps,
                key=lambda step: (
                    step.priority,
                    step.identifier,
                ),
            )
        )

    # ---------------------------------------------------------
    # Build
    # ---------------------------------------------------------

    def build(
        self,
    ) -> Pipeline:
        """
        Builds an immutable Pipeline.
        """
        return Pipeline(
            name=self._name,
            steps=self.ordered_steps,
        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        return self.step_count

    def __str__(
        self,
    ) -> str:
        return (
            f"{self.display_name}"
            f" ({self.step_count} steps)"
        )
