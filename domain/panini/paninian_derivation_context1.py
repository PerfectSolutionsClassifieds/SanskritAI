from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Context

Canonical immutable input context for the Pāṇinian
Derivation Pipeline.

This object represents the complete linguistic input
required before the derivational stages begin.

Unlike DerivationContext, this class is intended for the
full Aṣṭādhyāyī-style derivation process and therefore
remains stable throughout the pipeline while successive
PaninianDerivationState objects evolve.

Pipeline

PaninianDerivationContext
        │
        ▼
PaninianDerivationPipeline
        │
        ▼
PaninianDerivationState
        │
        ▼
Stage
        │
        ▼
Stage
        │
        ▼
Final Form

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.pratyaya.pratyaya_specification import (
    PratyayaSpecification,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PaninianDerivationContext(
    Displayable,
):
    """
    Immutable input for the Paninian Derivation Pipeline.

    This context never changes.

    Every derivational stage receives this same object,
    while modifying only the accompanying
    PaninianDerivationState.
    """

    identifier: str

    dhatu: Dhatu

    pratyaya: PratyayaSpecification

    metadata: dict[
        str,
        object,
    ] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return (
            "Paninian Derivation Context"
        )

    @property
    def display_text(
        self,
    ) -> str:
        return (
            f"{self.dhatu.root}"
            f" + "
            f"{self.pratyaya.pratyaya}"
        )

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Immutable linguistic input supplied to "
            "the Paninian Derivation Pipeline."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def dhatu_root(
        self,
    ) -> str:
        return self.dhatu.root

    @property
    def dhatu_meaning(
        self,
    ) -> str:
        return self.dhatu.meaning

    @property
    def pratyaya_name(
        self,
    ) -> str:
        return self.pratyaya.pratyaya

    @property
    def pratyaya_meaning(
        self,
    ) -> str:
        return self.pratyaya.meaning

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata
        )

    def metadata_value(
        self,
        key: str,
        default: object | None = None,
    ) -> object | None:
        """
        Returns a metadata value.
        """
        return self.metadata.get(
            key,
            default,
        )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
