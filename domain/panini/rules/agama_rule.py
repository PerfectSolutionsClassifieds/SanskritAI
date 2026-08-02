from __future__ import annotations

"""
SanskritAI
==========

Agama Rule

Canonical abstract base class for every Āgama rule.

An Āgama rule inserts one or more phonemes or morphemes into a
derivation.

Architecture
------------

PaninianRule
      │
      ▼
VidhiRule
      │
      ▼
AgamaRule
      │
      ▼
Concrete Āgama Sūtras

This class guarantees

    category  = VIDHI

    operation = AGAMA

Version
-------
v2.0.0
"""

from abc import ABC
from dataclasses import dataclass
from dataclasses import replace

from SanskritAI.domain.panini.paninian_rule_category import (
    PaninianRuleCategory,
)
from SanskritAI.domain.panini.paninian_rule_operation import (
    PaninianRuleOperation,
)
from SanskritAI.domain.panini.rules.vidhi_rule import (
    VidhiRule,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AgamaRule(
    VidhiRule,
    ABC,
):
    """
    Abstract base class for every Āgama rule.
    """

    def __post_init__(self) -> None:

        metadata = self.metadata

        if (
            metadata.category
            is not PaninianRuleCategory.VIDHI
            or
            metadata.operation
            is not PaninianRuleOperation.AGAMA
        ):
            metadata = replace(
                metadata,
                category=PaninianRuleCategory.VIDHI,
                operation=PaninianRuleOperation.AGAMA,
            )

            object.__setattr__(
                self,
                "metadata",
                metadata,
            )

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @property
    def is_agama(self) -> bool:
        return True

    @property
    def inserts_material(self) -> bool:
        return True

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def explain(self) -> str:
        return (
            "VIDHI : "
            "Āgama Operation"
        )
