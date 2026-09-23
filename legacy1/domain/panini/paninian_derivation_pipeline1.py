from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Pipeline

Canonical executable orchestration pipeline implementing the
Pāṇinian derivation process.

The pipeline itself is intentionally generic. It merely
coordinates execution of an ordered sequence of
PaninianDerivationStage objects.

Individual grammatical behaviour is implemented entirely
inside the stages.

Architecture
------------

Context
    │
    ▼
Initial State
    │
    ▼
Stage Collection
    │
    ├── Stage 1
    ├── Stage 2
    ├── Stage 3
    └── ...
    │
    ▼
Trace
    │
    ▼
PaninianDerivationResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)
from SanskritAI.domain.panini.paninian_derivation_result import (
    PaninianDerivationResult,
)
from SanskritAI.domain.panini.paninian_derivation_state import (
    PaninianDerivationState,
)
from SanskritAI.domain.panini.paninian_derivation_trace import (
    PaninianDerivationTrace,
)
from SanskritAI.domain.panini.paninian_stage_collection import (
    PaninianStageCollection,
)


@dataclass(slots=True)
class PaninianDerivationPipeline(Displayable):
    """
    Canonical executable Paninian derivation pipeline.
    """

    stages: PaninianStageCollection = field(
        default_factory=PaninianStageCollection,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Derivation Pipeline"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name}"
            f" ({self.stage_count} stages)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Executable orchestration pipeline for "
            "Paninian derivation."
        )

    # ---------------------------------------------------------
    # Inspection
    # ---------------------------------------------------------

    @property
    def stage_count(self) -> int:
        return self.stages.count

    @property
    def is_empty(self) -> bool:
        return self.stages.is_empty

    @property
    def is_not_empty(self) -> bool:
        return self.stages.is_not_empty

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def add_stage(
        self,
        stage,
    ) -> "PaninianDerivationPipeline":
        """
        Appends a stage to the pipeline.
        """
        self.stages = self.stages.add(stage)
        return self

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        context: PaninianDerivationContext,
    ) -> PaninianDerivationResult:
        """
        Executes the complete derivation pipeline.
        """

        state = PaninianDerivationState.initial(
            context,
        )

        trace = PaninianDerivationTrace().add(
            state,
        )

        diagnostics: list[str] = []

        for stage in self.stages:

            try:

                state = stage.execute(
                    context,
                    state,
                )

                trace = trace.add(
                    state,
                )

            except Exception as exc:

                diagnostics.append(
                    (
                        f"{stage.display_name}: "
                        f"{exc}"
                    )
                )

                return PaninianDerivationResult(
                    context=context,
                    final_state=state,
                    trace=trace,
                    succeeded=False,
                    confidence=0.0,
                    diagnostics=tuple(
                        diagnostics,
                    ),
                )

        confidence = 1.0

        if diagnostics:
            confidence = 0.75

        return PaninianDerivationResult(
            context=context,
            final_state=state,
            trace=trace,
            succeeded=True,
            confidence=confidence,
            diagnostics=tuple(
                diagnostics,
            ),
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __call__(
        self,
        context: PaninianDerivationContext,
    ) -> PaninianDerivationResult:
        return self.execute(
            context,
        )

    def __len__(self) -> int:
        return self.stage_count

    def __iter__(self):
        return iter(self.stages)

    def __str__(self) -> str:
        return self.display_text
