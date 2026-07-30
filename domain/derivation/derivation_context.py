from __future__ import annotations

"""
SanskritAI
==========

Derivation Context

Defines the canonical context for morphological derivation.

DerivationContext is the foundational value object of the
Morphological Derivation Kernel. Every derivational operation
begins with a DerivationContext, which encapsulates the core
linguistic inputs required to combine a Dhatu and a Pratyaya
into a derived form.

This class intentionally mirrors the structure used by the
Resolution, Sandhi, Samasa, Dhatu, and Pratyaya kernels while
remaining specific to complete word formation.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.pratyaya.pratyaya_factory import Pratyaya


@dataclass(frozen=True, slots=True)
class DerivationContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical context supplied to every derivational operation.
    """

    identifier: str

    dhatu: Dhatu

    pratyaya: Pratyaya

    source: str = ""

    language: str = "Sanskrit"

    script: str = "Devanagari"

    allow_multiple_derivations: bool = True

    enable_recursive_derivation: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return "Derivation Context"

    @property
    def display_text(self) -> str:
        return f"{self.dhatu.display_text} + {self.pratyaya.display_text}"

    @property
    def display_description(self) -> str:
        return "Canonical context for morphological derivation."

    @property
    def has_source(self) -> bool:
        return bool(self.source)

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    @property
    def metadata_count(self) -> int:
        return len(self.metadata)

    @property
    def recursive(self) -> bool:
        return self.enable_recursive_derivation

    @property
    def multiple_derivations_enabled(self) -> bool:
        return self.allow_multiple_derivations

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def __str__(self) -> str:
        return self.display_text
