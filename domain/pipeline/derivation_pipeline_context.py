from __future__ import annotations

"""
SanskritAI
==========

Derivation Pipeline Context

Immutable request object supplied to the Morphological
Derivation Pipeline.

Unlike DerivationContext (which represents only the Derivation
Kernel), this context represents the complete orchestration
request spanning multiple linguistic kernels.

Typical execution

    Dhātu
        ↓
    Pratyaya
        ↓
    Paninian Rule Engine
        ↓
    Derivation
        ↓
    Sandhi
        ↓
    Samāsa
        ↓
    Grammar
        ↓
    Semantics
        ↓
    Chandas
        ↓
    Alaṅkāra
        ↓
    Vākya
        ↓
    Knowledge Graph

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class DerivationPipelineContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable execution request for the Morphological
    Derivation Pipeline.
    """

    identifier: str

    subject: Any = None

    dhatu: Any | None = None

    pratyaya: Any | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    source: str = "pipeline"

    language: str = "sa"

    script: str = "Devanagari"

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Derivation Pipeline Context"

    @property
    def display_text(self) -> str:
        return self.identifier

    @property
    def display_description(self) -> str:
        return (
            "Execution context for the Morphological "
            "Derivation Pipeline."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_subject(self) -> bool:
        return self.subject is not None

    @property
    def has_dhatu(self) -> bool:
        return self.dhatu is not None

    @property
    def has_pratyaya(self) -> bool:
        return self.pratyaya is not None

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    @property
    def metadata_keys(
        self,
    ) -> tuple[str, ...]:
        return tuple(
            sorted(
                self.metadata.keys()
            )
        )

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Safe metadata lookup.
        """
        return self.metadata.get(
            key,
            default,
        )

    def with_metadata(
        self,
        **metadata: Any,
    ) -> "DerivationPipelineContext":
        """
        Returns a new immutable context containing the
        supplied metadata.
        """
        merged = dict(self.metadata)
        merged.update(metadata)

        return DerivationPipelineContext(
            identifier=self.identifier,
            subject=self.subject,
            dhatu=self.dhatu,
            pratyaya=self.pratyaya,
            metadata=merged,
            source=self.source,
            language=self.language,
            script=self.script,
        )

    def __str__(self) -> str:
        return self.display_text
