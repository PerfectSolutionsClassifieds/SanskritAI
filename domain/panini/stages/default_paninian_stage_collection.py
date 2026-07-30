from __future__ import annotations

"""
SanskritAI
==========

Default Paninian Stage Collection

Provides the canonical ordered sequence of Paninian
derivation stages used by the PaninianDerivationPipeline.

Purpose
-------
This class centralizes the construction of the derivation
pipeline, ensuring that stage ordering is defined in a
single location.

Benefits
--------
• Eliminates manual stage construction inside pipelines.
• Makes stage ordering configurable.
• Allows insertion, removal, or replacement of stages
  without modifying the pipeline implementation.
• Aligns with the architecture used by other SanskritAI
  kernels.

Canonical Order
---------------

Phase 1 — Preparation

    1. Dhātu Selection
    2. Pratyaya Selection
    3. It-Saṃjñā

Phase 2 — Core Derivation

    4. Aṅga Processing
    5. Guṇa–Vṛddhi
    6. Āgama
    7. Lopa
    8. Substitution (Ādeśa)

Phase 3 — Phonological Completion

    9. Sandhi
   10. Tripādī
   11. Final Form

Version
-------
v1.0.0
"""

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

#
# This import will become valid once FinalFormStage
# is implemented.
#
# from SanskritAI.domain.panini.stages.final_form_stage import (
#     FinalFormStage,
# )


class DefaultPaninianStageCollection(
    PaninianStageCollection,
):
    """
    Canonical Paninian derivation stage collection.
    """

    def __init__(
        self,
    ) -> None:

        super().__init__()

        #
        # Phase 1
        #

        self.append(
            DhatuSelectionStage(),
        )

        self.append(
            PratyayaSelectionStage(),
        )

        self.append(
            ItSamjnaStage(),
        )

        #
        # Phase 2
        #

        self.append(
            AngaProcessingStage(),
        )

        self.append(
            GunaVrddhiStage(),
        )

        self.append(
            AgamaStage(),
        )

        self.append(
            LopaStage(),
        )

        self.append(
            SubstitutionStage(),
        )

        #
        # Phase 3
        #

        self.append(
            SandhiStage(),
        )

        self.append(
            TripadiStage(),
        )

        #
        # Final stage
        #
        # Enable once implemented.
        #
        # self.append(
        #     FinalFormStage(),
        # )

    @classmethod
    def create(
        cls,
    ) -> "DefaultPaninianStageCollection":
        """
        Creates the canonical stage collection.
        """
        return cls()
