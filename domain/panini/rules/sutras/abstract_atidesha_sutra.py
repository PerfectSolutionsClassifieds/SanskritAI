from __future__ import annotations

"""
SanskritAI
==========

Abstract Atideśa Sūtra

Canonical executable base class for every
Atideśa (extension by analogy) sūtra of the
Aṣṭādhyāyī.

Purpose
-------

An Atideśa Sūtra extends an already established
grammatical property, operation, or behaviour to
another grammatical environment by analogy.

Unlike ordinary Vidhi rules, an Atideśa does not
normally introduce an entirely new grammatical
operation—it extends an existing one.

Therefore this class derives from
AbstractVidhiSutra.

Examples
--------

1.1.56
    स्थानिवदादेशोऽनल्विधौ

Responsibilities
----------------

• inherits the canonical Vidhi execution lifecycle

• performs extension by analogy

• standardises diagnostics

• standardises execution tracing

Future
------

Concrete Atideśa Sūtras will implement

    extend_property()

or

    perform_transformation()

depending upon the grammatical semantics.

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


class AbstractAtideshaSutra(
    AbstractVidhiSutra,
    ABC,
):
    """
    Canonical executable Atideśa Sūtra.
    """

    # ---------------------------------------------------------
    # Behaviour
    # ---------------------------------------------------------

    @property
    def behaviour(self) -> PaninianRuleBehaviour:
        """
        Extension by analogy.
        """
        return PaninianRuleBehaviour.EXTENSION

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def extension_name(self) -> str:
        """
        Human-readable extension.

        Concrete subclasses may override.
        """
        return self.sutra_text

    def explain(self) -> str:
        return (
            f"Atideśa Sūtra : "
            f"{self.sutra_number}"
            " — "
            f"{self.extension_name}"
        )

    def trace(self) -> dict:
        """
        Structured execution trace.
        """

        trace = super().trace()

        trace.update(
            {
                "behaviour": self.behaviour.value,
                "extension": self.extension_name,
            }
        )

        return trace

    # ---------------------------------------------------------
    # Classification helpers
    # ---------------------------------------------------------

    @property
    def is_extension_rule(self) -> bool:
        """
        Indicates that this rule performs an
        extension by analogy.
        """
        return True
