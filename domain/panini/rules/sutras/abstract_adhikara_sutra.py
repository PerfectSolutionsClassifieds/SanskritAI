from __future__ import annotations

"""
SanskritAI
==========

Abstract Adhikāra Sūtra

Canonical executable base class for every
Adhikāra (governing scope) sūtra of the
Aṣṭādhyāyī.

Purpose
-------

An Adhikāra Sūtra establishes the grammatical
scope under which subsequent sūtras operate.

Unlike Vidhi Sūtras, Adhikāra Sūtras generally
do not perform direct grammatical transformations.

Instead, they modify the derivational environment
by introducing a governing context.

Examples
--------

3.1.1      प्रत्ययः

2.1.3      प्राक्कडारात् समासः

Responsibilities
----------------

• inherits the canonical execution lifecycle

• establishes grammatical scope

• records contextual information

• provides uniform diagnostics

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.domain.panini.paninian_rule_behaviour import (
    PaninianRuleBehaviour,
)
from SanskritAI.domain.panini.rules.sutras.abstract_sutra import (
    AbstractSutra,
)


class AbstractAdhikaraSutra(
    AbstractSutra,
    ABC,
):
    """
    Canonical executable Adhikāra Sūtra.
    """

    # ---------------------------------------------------------
    # Behaviour
    # ---------------------------------------------------------

    @property
    def behaviour(self) -> PaninianRuleBehaviour:
        """
        Scope-establishing grammatical behaviour.
        """
        return PaninianRuleBehaviour.SCOPE

    # ---------------------------------------------------------
    # Applicability
    # ---------------------------------------------------------

    def supports(
        self,
        context,
    ) -> bool:
        """
        Adhikāra rules are generally globally applicable.

        Concrete subclasses may override.
        """
        return self.is_enabled

    # ---------------------------------------------------------
    # Semantic contract
    # ---------------------------------------------------------

    @abstractmethod
    def establish_scope(
        self,
        context,
    ) -> None:
        """
        Establishes the governing grammatical scope.

        Concrete subclasses implement this.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Canonical execution
    # ---------------------------------------------------------

    def _execute_rule(
        self,
        context,
    ) -> tuple:
        """
        Executes the Adhikāra semantics.
        """

        self.establish_scope(
            context,
        )

        return (context,)

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def scope_name(self) -> str:
        """
        Human-readable scope.

        Concrete subclasses may override.
        """
        return self.sutra_text

    def explain(self) -> str:
        return (
            f"Adhikāra Sūtra : "
            f"{self.sutra_number}"
            " — "
            f"{self.scope_name}"
        )

    def trace(self) -> dict:
        """
        Structured execution trace.
        """

        trace = super().trace()

        trace.update(
            {
                "behaviour": self.behaviour.value,
                "scope": self.scope_name,
            }
        )

        return trace

    # ---------------------------------------------------------
    # Classification helpers
    # ---------------------------------------------------------

    @property
    def is_scope_rule(self) -> bool:
        """
        Indicates that this rule establishes
        grammatical scope.
        """
        return True
