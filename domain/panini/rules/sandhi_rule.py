from __future__ import annotations

"""
SanskritAI
==========

Sandhi Rule

Canonical abstract base class for every Sandhi rule.

Sandhi rules perform phonological transformations at the
junction of sounds.

Architecture
------------

PaninianRule
      │
      ▼
VidhiRule
      │
      ▼
SandhiRule
      │
      ▼
Concrete Sandhi Sūtras

This class guarantees

    category  = VIDHI

    operation = SANDHI

Examples
--------

6.1.77  iko yaṇ aci

6.1.87  ādguṇaḥ

6.1.88  vṛddhireci

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
class SandhiRule(
    VidhiRule,
    ABC,
):
    """
    Abstract base class for every Sandhi rule.
    """

    def __post_init__(self) -> None:

        metadata = self.metadata

        if (
            metadata.category
            is not PaninianRuleCategory.VIDHI
            or
            metadata.operation
            is not PaninianRuleOperation.SANDHI
        ):
            metadata = replace(
                metadata,
                category=PaninianRuleCategory.VIDHI,
                operation=PaninianRuleOperation.SANDHI,
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
    def is_sandhi(self) -> bool:
        return True

    @property
    def is_phonological(self) -> bool:
        return True

    @property
    def performs_phonological_transformation(self) -> bool:
        return True

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def explain(self) -> str:
        return (
            "VIDHI : "
            "Sandhi (Phonological Transformation)"
        )
