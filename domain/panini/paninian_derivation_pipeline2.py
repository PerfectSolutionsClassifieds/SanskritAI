from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Pipeline

Canonical executable derivation pipeline.

This implementation is intentionally lightweight.

Rather than embedding grammatical logic, it orchestrates a
configurable sequence of PaninianDerivationStage objects using
PaninianStageCollection while leveraging the reusable Pipeline
framework already established under SanskritAI.core.pipeline.

Pipeline

    Dhātu Selection
            ↓
    Pratyaya Selection
            ↓
    It-Saṃjñā
            ↓
    Aṅga Processing
            ↓
    Guṇa–Vṛddhi
            ↓
    Āgama
            ↓
    Lopa
            ↓
    Substitution
            ↓
    Sandhi
            ↓
    Tripādī

Version
-------
v2.0.0
"""

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

from SanskritAI.domain.panini.stages.dhatu_selection_stage import (
    DhatuSelectionStage,
)
from SanskritAI.domain.panini.stages.pratyaya_selection_stage import (
    PratyayaSelectionStage,
)
from SanskritAI.domain.panini.stages.it_samjna_stage import (
    ItSamjnaStage,
)
from SanskritAI.domain.panini.stages.anga_processing_stage import (
    AngaProcessingStage,
)
from SanskritAI.domain.panini.stages.guna_vrddhi_stage import (
    GunaVrddhiStage,
)
from SanskritAI.domain.panini.stages.agama_stage import (
    AgamaStage,
)
from SanskritAI.domain.panini.stages.lopa_stage import (
    LopaStage,
)
from SanskritAI.domain.panini.stages.substitution_stage import (
    SubstitutionStage,
)
from SanskritAI.domain.panini.stages.sandhi_stage import (
    SandhiStage,
)
from SanskritAI.domain.panini.stages.tripadi_stage import (
    TripadiStage,
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
        default_factory=PaninianStageCollection,
    )

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __post_init__(self) -> None:

        #
        # Populate only if user did not provide stages.
        #
        if len(self.stage_collection) == 0:

            self.stage_collection.extend(
                [
                    DhatuSelectionStage(),
                    PratyayaSelectionStage(),
                    ItSamjnaStage(),
                    AngaProcessingStage(),
                    GunaVrddhiStage(),
                    AgamaStage(),
                    LopaStage(),
                    SubstitutionStage(),
                    SandhiStage(),
                    TripadiStage(),
                ]
            )

    # ---------------------------------------------------------
    # Pipeline metadata
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
            "Executable Paninian derivation pipeline "
            "built from reusable derivation stages."
        )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        context: PaninianDerivationContext,
    ) -> PaninianDerivationResult:
        """
        Executes every registered Paninian stage.
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
                metadata=dict(state.metadata),
            )

        return PaninianDerivationResult(
            context=context,
            final_state=state,
            trace=trace,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def add_stage(
        self,
        stage,
    ) -> "PaninianDerivationPipeline":
        """
        Adds a stage to the pipeline.
        """

        self.stage_collection.append(stage)
        return self

    def remove_stage(
        self,
        stage_type,
    ) -> "PaninianDerivationPipeline":
        """
        Removes all stages of a given type.
        """

        self.stage_collection[:] = [
            s
            for s in self.stage_collection
            if not isinstance(s, stage_type)
        ]

        return self

    @property
    def stages(self):
        return tuple(self.stage_collection)

    @property
    def stage_count(self) -> int:
        return len(self.stage_collection)

    def __len__(self) -> int:
        return self.stage_count

    def __iter__(self):
        return iter(self.stage_collection)

    def __str__(self) -> str:
        return (
            f"{self.display_name}"
            f" ({self.stage_count} stages)"
        )
