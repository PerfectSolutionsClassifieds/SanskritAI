from __future__ import annotations

"""
SanskritAI
==========

Visarga Transformation Rule

Abstract base class for Sandhi rules that transform a
terminal Visarga (ः) into another phonological realization.

These rules preserve the identity of Visarga while changing
its surface manifestation according to Paninian grammar.

Typical examples
----------------

    ः → स
    ः → र

Hierarchy
---------

SandhiRule
    │
    ▼
VisargaSandhiRule
    │
    ▼
VisargaTransformationRule
    │
    ├── VisargaToSRule
    └── VisargaToRRule

Version
-------
v1.0.0
"""

from abc import abstractmethod

from SanskritAI.domain.sandhi.visarga_sandhi_rule import (
    VisargaSandhiRule,
)


class VisargaTransformationRule(
    VisargaSandhiRule,
):
    """
    Base class for Visarga transformation rules.

    Transformation rules replace Visarga with another
    phoneme while preserving the grammatical identity of
    the Visarga.
    """

    @property
    def display_name(self) -> str:
        return "Visarga Transformation Rule"

    @property
    def display_description(self) -> str:
        return (
            "Abstract base class for Visarga "
            "transformation rules."
        )

    @property
    def is_transformation_rule(self) -> bool:
        return True

    @property
    def is_allophone_rule(self) -> bool:
        return False

    @abstractmethod
    def applies_to(self, context):
        """
        Determines whether the transformation rule applies.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(self, context):
        """
        Applies the Visarga transformation.
        """
        raise NotImplementedError
