from __future__ import annotations

"""
SanskritAI
==========

Abstract Niyama Sūtra

Canonical executable base class for every
Niyama (restrictive) sūtra of the Aṣṭādhyāyī.

Purpose
-------

A Niyama Sūtra does not introduce a new grammatical
operation.

Instead, it restricts the application of an
otherwise valid Vidhi.

Therefore this class derives from
AbstractVidhiSutra.

Examples
--------

1.4.14

...

Responsibilities
----------------

• inherits the canonical Vidhi execution model

• restricts grammatical applicability

• provides uniform diagnostics

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.panini.paninian_rule_behaviour import (
    PaninianRuleBehaviour,
)
from SanskritAI.domain.panini.rules.sutras.abstract_vidhi_sutra import (
    AbstractVidhiSutra,
)


class AbstractNiyamaSutra(
    AbstractVidhiSutra,
    ABC,
):
    """
    Canonical executable Niyama Sūtra.
    """

    # ---------------------------------------------------------
    # Behaviour
    # ---------------------------------------------------------

    @property
    def behaviour(self) -> PaninianRuleBehaviour:
        """
        Restrictive grammatical behaviour.
        """
        return PaninianRuleBehaviour.RESTRICTION

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def restriction_name(self) -> str:
        """
        Human-readable restriction.

        Concrete subclasses may override.
        """
        return self.sutra_text

    def explain(self) -> str:
        return (
            f"Niyama Sūtra : "
            f"{self.sutra_number}"
            " — "
            f"{self.restriction_name}"
        )

    def trace(self) -> dict:

        trace = super().trace()

        trace.update(
            {
                "behaviour": self.behaviour.value,
                "restriction": self.restriction_name,
            }
        )

        return trace
