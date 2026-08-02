from __future__ import annotations

"""
SanskritAI
==========

Lopa Rule

Canonical abstract base class for every Lopa rule.

A Lopa rule removes (elides) one or more phonemes, markers,
or grammatical elements from a derivation.

Architecture
------------

PaninianRule
      │
      ▼
VidhiRule
      │
      ▼
LopaRule
      │
      ▼
Concrete Lopa Sūtras

This class guarantees

    category  = VIDHI

    operation = LOPA

Examples
--------

1.3.9  tasya lopaḥ

Future
------

Concrete subclasses will implement specific Paninian
lopa sūtras.

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
class LopaRule(
    VidhiRule,
    ABC,
):
    """
    Abstract base class for every Lopa rule.
    """

    def __post_init__(self) -> None:
        """
        Ensures every LopaRule always represents

            Category  : VIDHI

            Operation : LOPA
        """

        metadata = self.metadata

        if (
            metadata.category
            is not PaninianRuleCategory.VIDHI
            or
            metadata.operation
            is not PaninianRuleOperation.LOPA
        ):
            metadata = replace(
                metadata,
                category=PaninianRuleCategory.VIDHI,
                operation=PaninianRuleOperation.LOPA,
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
    def is_lopa(self) -> bool:
        """
        Indicates that this is a Lopa rule.
        """
        return True

    @property
    def deletes_material(self) -> bool:
        """
        Lopa removes linguistic material.
        """
        return True

    @property
    def performs_elision(self) -> bool:
        """
        Convenience alias.
        """
        return True

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def explain(self) -> str:
        """
        Human-readable explanation.
        """
        return (
            "VIDHI : "
            "Lopa (Elision) Operation"
        )
