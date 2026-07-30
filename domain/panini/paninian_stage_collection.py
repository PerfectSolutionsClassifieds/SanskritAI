from __future__ import annotations

"""
SanskritAI
==========

Paninian Stage Collection

Immutable ordered collection of PaninianDerivationStage
objects.

The collection preserves the canonical ordering of the
Pāṇinian derivation process while providing convenient
functional operations for building pipelines.

Typical order

    Dhātu Stage
        ↓
    Pratyaya Stage
        ↓
    It-Saṃjñā Stage
        ↓
    Aṅga Stage
        ↓
    Guṇa / Vṛddhi Stage
        ↓
    Sandhi Stage
        ↓
    Tripādī Stage
        ↓
    Final Form Stage

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.panini.paninian_derivation_stage import (
    PaninianDerivationStage,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PaninianStageCollection(
    Displayable,
):
    """
    Immutable ordered collection of Paninian derivation stages.
    """

    stages: tuple[
        PaninianDerivationStage,
        ...
    ] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Stage Collection"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name}"
            f" ({self.count} stages)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable ordered collection of "
            "Paninian derivation stages."
        )

    # ---------------------------------------------------------
    # Inspection
    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        return len(self.stages)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def is_not_empty(self) -> bool:
        return not self.is_empty

    @property
    def first(self) -> PaninianDerivationStage | None:
        if self.is_empty:
            return None
        return self.stages[0]

    @property
    def last(self) -> PaninianDerivationStage | None:
        if self.is_empty:
            return None
        return self.stages[-1]

    @property
    def stage_names(
        self,
    ) -> tuple[str, ...]:
        return tuple(
            stage.display_name
            for stage in self.stages
        )

    # ---------------------------------------------------------
    # Functional updates
    # ---------------------------------------------------------

    def add(
        self,
        stage: PaninianDerivationStage,
    ) -> "PaninianStageCollection":
        """
        Returns a new collection with one additional stage.
        """
        return PaninianStageCollection(
            stages=(
                *self.stages,
                stage,
            )
        )

    def extend(
        self,
        stages: tuple[
            PaninianDerivationStage,
            ...
        ],
    ) -> "PaninianStageCollection":
        """
        Returns a new collection with additional stages.
        """
        return PaninianStageCollection(
            stages=(
                *self.stages,
                *stages,
            )
        )

    def insert(
        self,
        index: int,
        stage: PaninianDerivationStage,
    ) -> "PaninianStageCollection":
        """
        Inserts a stage at the specified position.
        """
        updated = list(self.stages)
        updated.insert(
            index,
            stage,
        )

        return PaninianStageCollection(
            stages=tuple(updated),
        )

    def remove(
        self,
        stage_name: str,
    ) -> "PaninianStageCollection":
        """
        Removes every stage whose display name matches.
        """
        return PaninianStageCollection(
            stages=tuple(
                stage
                for stage in self.stages
                if stage.display_name != stage_name
            )
        )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def contains(
        self,
        stage_name: str,
    ) -> bool:
        return any(
            stage.display_name == stage_name
            for stage in self.stages
        )

    def find(
        self,
        stage_name: str,
    ) -> PaninianDerivationStage | None:
        for stage in self.stages:
            if stage.display_name == stage_name:
                return stage

        return None

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(self):
        return iter(self.stages)

    def __len__(self) -> int:
        return self.count

    def __getitem__(
        self,
        index: int,
    ) -> PaninianDerivationStage:
        return self.stages[index]

    def __contains__(
        self,
        stage_name: str,
    ) -> bool:
        return self.contains(stage_name)

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
