from __future__ import annotations

"""
SanskritAI
==========

Visarga Allophone Rule

Abstract base class for Visarga rules that realize the
Visarga as one of its phonetic allophones.

Unlike transformation rules, these rules do not replace the
grammatical identity of Visarga. They merely determine its
phonetic realization.

Typical examples
----------------

    ः → Jihvāmūlīya   (before क् / ख्)

    ः → Upadhmānīya  (before प् / फ्)

Hierarchy
---------

SandhiRule
    │
    ▼
VisargaSandhiRule
    │
    ▼
VisargaAllophoneRule
    │
    ├── JihvamuliyaRule
    └── UpadhmaniyaRule

Version
-------
v1.0.0
"""

from abc import abstractmethod

from SanskritAI.domain.sandhi.visarga_sandhi_rule import (
    VisargaSandhiRule,
)


class VisargaAllophoneRule(
    VisargaSandhiRule,
):
    """
    Base class for Visarga allophonic realization rules.

    These rules determine the phonetic realization of a
    Visarga without changing its grammatical identity.
    """

    @property
    def display_name(self) -> str:
        return "Visarga Allophone Rule"

    @property
    def display_description(self) -> str:
        return (
            "Abstract base class for Visarga "
            "allophonic realization rules."
        )

    @property
    def is_transformation_rule(self) -> bool:
        return False

    @property
    def is_allophone_rule(self) -> bool:
        return True

    @abstractmethod
    def applies_to(self, context):
        """
        Determines whether the allophone rule applies.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(self, context):
        """
        Applies the allophonic realization.
        """
        raise NotImplementedError
