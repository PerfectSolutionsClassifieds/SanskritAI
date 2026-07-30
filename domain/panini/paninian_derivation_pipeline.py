from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Pipeline

Canonical executable implementation of the complete
Pāṇinian derivation process.

Unlike previous versions, this implementation no longer
constructs stages itself.

Instead, it delegates stage construction to

    DefaultPaninianStageCollection

which becomes the single authoritative definition of the
Paninian derivation workflow.

Architecture

PaninianDerivationPipeline
            │
            ▼
DefaultPaninianStageCollection
            │
            ▼
PaninianRuleDrivenStage
            │
            ▼
PaninianRuleEngine
            │
            ▼
PaninianRuleSet
            │
            ▼
PaninianRule

Version
-------
v3.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.pipeline.pipeline import Pipeline

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

from SanskritAI.domain.panini.stages.default_paninian_stage_collection import (
    DefaultPaninianStageCollection,
)


@dataclass(slots=True)
class PaninianDerivationPipeline(
    Pipeline,
    Displayable,
):
    """
    Canonical executable Paninian derivation pipeline.
    """

    stage_collection: PaninianStageCollection = field(
        default_factory=DefaultPaninianStageCollection,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def name(self) -> str:
        return "Paninian Derivation Pipeline"

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_description(self) -> str:
        return (
            "Canonical executable Paninian derivation "
            "pipeline."
        )

    # ---------------------------------------------------------
    # Pipeline Execution
    # ---------------------------------------------------------

    def execute(
        self,
        context: PaninianDerivationContext,
    ) -> PaninianDerivationResult:
        """
        Executes the canonical Paninian derivation.
        """

        state = PaninianDerivationState()

        trace = PaninianDerivationTrace()

        for stage in self.stage_collection:

            if not stage.is_applicable(
                context,
                state,
            ):
                continue

            previous_form = state.current_form

            state = stage.apply(
                context,
                state,
            )

            trace.record(
                stage_name=stage.display_name,
                input_form=previous_form,
                output_form=state.current_form,
                metadata=dict(
                    state.metadata,
                ),
            )

        return PaninianDerivationResult(
            context=context,
            final_state=state,
            trace=trace,
        )

    # ---------------------------------------------------------
    # Stage Manipulation
    # ---------------------------------------------------------

    def add_stage(
        self,
        stage,
    ) -> "PaninianDerivationPipeline":
        """
        Appends a stage to the pipeline.
        """

        self.stage_collection.append(
            stage,
        )

        return self

    def insert_stage(
        self,
        index: int,
        stage,
    ) -> "PaninianDerivationPipeline":
        """
        Inserts a stage into the pipeline.
        """

        self.stage_collection.insert(
            index,
            stage,
        )

        return self

    def remove_stage(
        self,
        stage_type,
    ) -> "PaninianDerivationPipeline":
        """
        Removes every stage of the given type.
        """

        retained = [
            stage
            for stage in self.stage_collection
            if not isinstance(
                stage,
                stage_type,
            )
        ]

        self.stage_collection.clear()

        self.stage_collection.extend(
            retained,
        )

        return self

    def replace_stage(
        self,
        stage_type,
        replacement,
    ) -> "PaninianDerivationPipeline":
        """
        Replaces the first matching stage.
        """

        for index, stage in enumerate(
            self.stage_collection
        ):
            if isinstance(
                stage,
                stage_type,
            ):
                self.stage_collection[index] = (
                    replacement
                )
                break

        return self

    # ---------------------------------------------------------
    # Inspection
    # ---------------------------------------------------------

    @property
    def stages(
        self,
    ):
        return tuple(
            self.stage_collection
        )

    @property
    def stage_count(
        self,
    ) -> int:
        return len(
            self.stage_collection
        )

    def __len__(
        self,
    ) -> int:
        return self.stage_count

    def __iter__(
        self,
    ):
        return iter(
            self.stage_collection
        )

    def __str__(
        self,
    ) -> str:
        return (
            f"{self.display_name}"
            f" ({self.stage_count} stages)"
        )
