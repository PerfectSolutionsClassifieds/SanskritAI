from __future__ import annotations

"""
SanskritAI
==========

Paninian Sūtra

Canonical immutable representation of one sūtra of the
Aṣṭādhyāyī.

A PaninianSutra is a textual scholarly object.

It is intentionally independent of executable grammar rules.

Multiple executable PaninianRule implementations may reference
the same PaninianSutra.

Architecture
------------

                PaninianSutra
                      │
          ┌───────────┼────────────┐
          │           │            │
     PaninianRule   Commentary   Knowledge Graph
          │
          ▼
    Executable Grammar

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(
    frozen=True,
    slots=True,
)
class PaninianSutra(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical representation of one Paninian sūtra.
    """

    identifier: str

    sutra_number: str

    sutra_text: str

    transliteration: str = ""

    translation: str = ""

    adhyaya: int = 0

    pada: int = 0

    source: str = "Aṣṭādhyāyī"

    commentary_references: tuple[str, ...] = field(
        default_factory=tuple,
    )

    notes: str = ""

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.sutra_number

    @property
    def display_text(self) -> str:
        if self.sutra_text:
            return (
                f"{self.sutra_number}"
                f" — "
                f"{self.sutra_text}"
            )
        return self.sutra_number

    @property
    def display_description(self) -> str:
        return self.translation

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def canonical_location(self) -> str:
        if self.adhyaya <= 0:
            return ""

        return (
            f"{self.adhyaya}"
            "."
            f"{self.pada}"
        )

    @property
    def has_translation(self) -> bool:
        return bool(self.translation)

    @property
    def has_transliteration(self) -> bool:
        return bool(self.transliteration)

    @property
    def has_commentaries(self) -> bool:
        return len(self.commentary_references) > 0

    @property
    def commentary_count(self) -> int:
        return len(self.commentary_references)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
