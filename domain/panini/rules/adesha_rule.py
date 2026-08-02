from __future__ import annotations

"""
SanskritAI
==========

Adesha Rule

Canonical abstract base class for every Ādeśa rule.

An Ādeśa rule replaces one linguistic element with another.

Architecture
------------

PaninianRule
      │
      ▼
VidhiRule
      │
      ▼
AdeshaRule
      │
      ▼
Concrete Ādeśa Sūtras

This class guarantees

    category  = VIDHI

    operation = ADESHA

Examples
--------

6.1.77  iko yaṇ aci

1.1.56  sthānivadādeśo'nalvidhau

Future
------

Concrete subclasses will implement individual Ādeśa
sūtras from the Aṣṭādhyāyī.

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
class AdeshaRule(
    VidhiRule,
    ABC,
):
    """
    Abstract base class for every Ādeśa rule.
    """

    def __post_init__(self) -> None:
        """
        Ensures every AdeshaRule always represents

            Category  : VIDHI

            Operation : ADESHA
        """

        metadata = self.metadata

        if (
            metadata.category
            is not PaninianRuleCategory.VIDHI
            or
            metadata.operation
            is not PaninianRuleOperation.ADESHA
        ):
            metadata = replace(
                metadata,
                category=PaninianRuleCategory.VIDHI,
                operation=PaninianRuleOperation.ADESHA,
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
    def is_adesha(self) -> bool:
        """
        Indicates that this is an Ādeśa rule.
        """
        return True

    @property
    def performs_substitution(self) -> bool:
        """
        Ādeśa performs substitution.
        """
        return True

    @property
    def replaces_material(self) -> bool:
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
            "Ādeśa (Substitution) Operation"
        )
