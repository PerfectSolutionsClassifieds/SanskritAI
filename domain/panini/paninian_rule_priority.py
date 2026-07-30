from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Priority

Defines the execution priority of Paninian rules.

Unlike

    • PaninianRuleCategory
    • PaninianRuleType

which describe *what* a rule is and *how* it behaves,

PaninianRulePriority determines

    "When should this rule execute relative to other
    applicable rules?"

This enumeration provides the foundation for deterministic
rule scheduling and future conflict resolution.

Typical uses include

    • Rule ordering
    • Apavāda over Utsarga resolution
    • Rule engine scheduling
    • Pipeline diagnostics

Version
-------
v1.0.0
"""

from enum import IntEnum
from enum import unique


@unique
class PaninianRulePriority(IntEnum):
    """
    Canonical execution priority for Paninian rules.

    Higher numeric values represent higher execution
    precedence.
    """

    # ---------------------------------------------------------
    # Lowest priorities
    # ---------------------------------------------------------

    LOWEST = 100

    LOW = 250

    NORMAL = 500

    HIGH = 750

    HIGHEST = 1000

    # ---------------------------------------------------------
    # Canonical Paninian priorities
    # ---------------------------------------------------------

    UTSARGA = 600

    APAVADA = 900

    PARIBHASHA = 950

    ADHIKARA = 975

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return {
            self.LOWEST: "Lowest",
            self.LOW: "Low",
            self.NORMAL: "Normal",
            self.HIGH: "High",
            self.HIGHEST: "Highest",
            self.UTSARGA: "Utsarga",
            self.APAVADA: "Apavāda",
            self.PARIBHASHA: "Paribhāṣā",
            self.ADHIKARA: "Adhikāra",
        }[self]

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @property
    def is_default_priority(self) -> bool:
        """
        Returns True if this is the normal scheduling
        priority.
        """
        return self is self.NORMAL

    @property
    def is_exception_priority(self) -> bool:
        """
        Returns True if this priority typically overrides
        default rules.
        """
        return self in {
            self.APAVADA,
            self.PARIBHASHA,
            self.ADHIKARA,
        }

    @property
    def is_high_priority(self) -> bool:
        """
        Returns True if this priority executes before
        normal rules.
        """
        return self >= self.HIGH

    @property
    def is_low_priority(self) -> bool:
        """
        Returns True if this priority executes after
        normal rules.
        """
        return self <= self.LOW

    @classmethod
    def default(cls) -> "PaninianRulePriority":
        """
        Returns the default execution priority.
        """
        return cls.NORMAL

    @classmethod
    def highest(cls) -> "PaninianRulePriority":
        """
        Returns the highest execution priority.
        """
        return cls.HIGHEST

    @classmethod
    def lowest(cls) -> "PaninianRulePriority":
        """
        Returns the lowest execution priority.
        """
        return cls.LOWEST

    def __str__(self) -> str:
        return self.display_name
