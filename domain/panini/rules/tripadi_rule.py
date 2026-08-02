from __future__ import annotations

"""
SanskritAI
==========

Tripadi Rule

Canonical abstract base class for every Tripādī rule.

Tripādī rules belong primarily to the eighth chapter of the
Aṣṭādhyāyī and are applied after the Sapādasaptādhyāyī.

Architecture
------------

PaninianRule
      │
      ▼
VidhiRule
      │
      ▼
TripadiRule
      │
      ▼
Concrete Tripādī Sūtras

This class guarantees

    category  = VIDHI

    operation = TRIPADI

Examples
--------

8.2.xx

8.3.xx

8.4.xx

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
class TripadiRule(
    VidhiRule,
    ABC,
):
    """
    Abstract base class for every Tripādī rule.
    """

    def __post_init__(self) -> None:

        metadata = self.metadata

        if (
            metadata.category
            is not PaninianRuleCategory.VIDHI
            or
            metadata.operation
            is not PaninianRuleOperation.TRIPADI
        ):
            metadata = replace(
                metadata,
                category=PaninianRuleCategory.VIDHI,
                operation=PaninianRuleOperation.TRIPADI,
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
    def is_tripadi(self) -> bool:
        return True

    @property
    def is_phonological(self) -> bool:
        return True

    @property
    def executes_after_sapadasaptadhyayi(self) -> bool:
        """
        Tripādī executes after the first seven chapters
        according to the traditional derivational order.
        """
        return True

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def explain(self) -> str:
        return (
            "VIDHI : "
            "Tripādī Rule"
        )
