from __future__ import annotations

"""
SanskritAI
==========

Pipeline Registry

Maintains the canonical registry of reusable Pipeline
instances.

The registry is intentionally kernel-independent and serves as
the central discovery mechanism for every Pipeline within
SanskritAI.

Typical registrations include

    • Derivation Pipeline
    • Semantic Pipeline
    • Vakya Pipeline
    • Chandas Pipeline
    • Alankara Pipeline
    • Knowledge Graph Pipeline

The PipelineFactory will later use this registry to construct
higher-level orchestration pipelines.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.pipeline.pipeline import Pipeline


@dataclass(slots=True)
class PipelineRegistry(Displayable):
    """
    Registry of reusable pipelines.
    """

    _pipelines: dict[str, Pipeline] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Pipeline Registry"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name}"
            f" ({self.pipeline_count} pipelines)"
        )

    @property
    def display_description(self) -> str:
        return "Registry of reusable Pipeline objects."

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        pipeline: Pipeline,
        *,
        overwrite: bool = False,
    ) -> "PipelineRegistry":
        """
        Registers a Pipeline.

        Raises
        ------
        ValueError
            If a pipeline with the same name already exists
            and overwrite=False.
        """

        key = pipeline.name.strip()

        if (
            key in self._pipelines
            and not overwrite
        ):
            raise ValueError(
                f"Pipeline '{key}' is already registered."
            )

        self._pipelines[key] = pipeline

        return self

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Removes a registered pipeline.
        """
        self._pipelines.pop(name, None)

    def clear(self) -> None:
        """
        Removes every registered pipeline.
        """
        self._pipelines.clear()

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
        return self._pipelines.get(name)

    def require(
        self,
        name: str,
    ) -> Pipeline:
        """
        Returns a registered Pipeline.

        Raises
        ------
        KeyError
            If the pipeline is not registered.
        """
        pipeline = self.get(name)

        if pipeline is None:
            raise KeyError(
                f"Pipeline '{name}' is not registered."
            )

        return pipeline

    def contains(
        self,
        name: str,
    ) -> bool:
        """
        Returns True if the pipeline exists.
        """
        return name in self._pipelines

    # ---------------------------------------------------------
    # Inspection
    # ---------------------------------------------------------

    @property
    def pipelines(
        self,
    ) -> tuple[Pipeline, ...]:
        return tuple(self._pipelines.values())

    @property
    def names(
        self,
    ) -> tuple[str, ...]:
        return tuple(sorted(self._pipelines.keys()))

    @property
    def pipeline_count(self) -> int:
        return len(self._pipelines)

    @property
    def is_empty(self) -> bool:
        return self.pipeline_count == 0

    @property
    def is_not_empty(self) -> bool:
        return not self.is_empty

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(self):
        return iter(self.pipelines)

    def __len__(self) -> int:
        return self.pipeline_count

    def __contains__(
        self,
        name: str,
    ) -> bool:
        return self.contains(name)

    def __str__(self) -> str:
        return self.display_text
