from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule

Defines the canonical base class for every Paninian grammatical
rule used throughout SanskritAI.

This class is intentionally kernel-independent. Every linguistic
kernel (Sandhi, Samāsa, Dhātu, Pratyaya, Derivation, Grammar,
Vakya, Semantics, Chandas, Alaṅkāra, etc.) may derive concrete
rules from this base class.

Architecture
------------

PaninianRule
      │
      ├── SandhiRule
      ├── SamasaRule
      ├── DhatuRule
      ├── PratyayaRule
      ├── DerivationRule
      ├── GrammarRule
      ├── VakyaRule
      ├── SemanticRule
      ├── ChandasRule
      └── AlankaraRule

Future
------

Each rule may later be linked to

• Mahābhāṣya

• Kāśikā

• Siddhānta Kaumudī

• Amarakośa

• Knowledge Graph

• Explainable AI traces

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PaninianRule(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Canonical Paninian rule.

    Concrete subclasses implement the apply() method.
    """

    identifier: str

    sutra_number: str

    sutra: str

    transliteration: str = ""

    english: str = ""

    adhyaya: int = 0

    pada: int = 0

    category: str = ""

    priority: int = 100

    dependencies: tuple[str, ...] = field(
        default_factory=tuple
    )

    references: tuple[str, ...] = field(
        default_factory=tuple
    )

    explanation: str = ""

    enabled: bool = True

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.sutra_number

    @property
    def display_text(self) -> str:
        if self.sutra:
            return (
                f"{self.sutra_number} — "
                f"{self.sutra}"
            )
        return self.sutra_number

    @property
    def display_description(self) -> str:
        return self.english

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def canonical_reference(self) -> str:
        return self.sutra_number

    @property
    def location(self) -> str:
        if self.adhyaya <= 0:
            return ""
        return f"{self.adhyaya}.{self.pada}"

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    @property
    def has_dependencies(self) -> bool:
        return len(self.dependencies) > 0

    @property
    def dependency_count(self) -> int:
        return len(self.dependencies)

    @property
    def has_references(self) -> bool:
        return len(self.references) > 0

    @property
    def reference_count(self) -> int:
        return len(self.references)

    # ---------------------------------------------------------
    # Matching
    # ---------------------------------------------------------

    def supports(
        self,
        context: Any,
    ) -> bool:
        """
        Determines whether this rule is applicable.

        Concrete subclasses may override.
        """
        return self.enabled

    # ---------------------------------------------------------
    # Rule execution
    # ---------------------------------------------------------

    @abstractmethod
    def apply(
        self,
        context: Any,
    ) -> tuple[Any, ...]:
        """
        Applies the Paninian rule.

        Returns
        -------
        tuple[Any, ...]

        Zero or more candidate outputs.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def __lt__(
        self,
        other: "PaninianRule",
    ) -> bool:
        return self.priority < other.priority

    def __str__(self) -> str:
        return self.display_text
