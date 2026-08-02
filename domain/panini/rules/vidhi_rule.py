from __future__ import annotations

"""
SanskritAI
==========

Vidhi Rule

Canonical abstract base class for every operational
(Prescriptive) Paninian rule.

A Vidhi rule performs an actual grammatical operation.

Examples

    • Āgama
    • Lopa
    • Ādeśa
    • Sandhi
    • Tripādī
    • Pratyaya
    • Samāsa

Architecture
------------

PaninianRule
      │
      ▼
VidhiRule
      │
      ├── AgamaRule
      ├── LopaRule
      ├── AdeshaRule
      ├── SandhiRule
      ├── TripadiRule
      └── ...

Responsibilities
----------------

This class guarantees that every subclass belongs to the
classical Paninian category

    VIDHI

while allowing subclasses to specify their own grammatical
operation.

Version
-------
v2.0.0
"""

from abc import ABC
from dataclasses import dataclass
from dataclasses import replace

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)
from SanskritAI.domain.panini.paninian_rule_category import (
    PaninianRuleCategory,
)
from SanskritAI.domain.panini.paninian_rule_metadata import (
    PaninianRuleMetadata,
)


@dataclass(
    frozen=True,
    slots=True,
)
class VidhiRule(
    PaninianRule,
    ABC,
):
    """
    Abstract base class for every Vidhi rule.
    """

    def __post_init__(self) -> None:
        """
        Ensures the metadata always belongs to the
        classical VIDHI category.
        """

        if (
            self.metadata.category
            is not PaninianRuleCategory.VIDHI
        ):
            object.__setattr__(
                self,
                "metadata",
                replace(
                    self.metadata,
                    category=PaninianRuleCategory.VIDHI,
                ),
            )

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @property
    def is_vidhi(self) -> bool:
        return True

    @property
    def is_operational(self) -> bool:
        return True

    @property
    def performs_transformation(self) -> bool:
        return self.metadata.has_operation

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def explain(self) -> str:
        return (
            f"VIDHI : "
            f"{self.metadata.operation.display_name}"
        )
