from __future__ import annotations

"""
SanskritAI
==========

Abstract Saṃjñā Sūtra

Canonical base class for every executable Saṃjñā
(technical definition) sūtra.

Examples
--------

1.1.1  vṛddhir ādaic

1.1.2  adeṅ guṇaḥ

1.1.3  iko guṇavṛddhī

Responsibilities
----------------

• Inherits the canonical execution lifecycle
  from AbstractSutra.

• Defines the execution model for grammatical
  designations (saṃjñā).

• Leaves only the designation semantics to
  concrete subclasses.

Version
-------
v2.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.domain.panini.rules.sutras.abstract_sutra import (
    AbstractSutra,
)


class AbstractSamjnaSutra(
    AbstractSutra,
    ABC,
):
    """
    Canonical executable Saṃjñā sūtra.
    """

    # ---------------------------------------------------------
    # Applicability
    # ---------------------------------------------------------

    def supports(
        self,
        context,
    ) -> bool:
        """
        Saṃjñā rules are normally always applicable.

        Individual sūtras may override.
        """
        return self.is_enabled

    # ---------------------------------------------------------
    # Semantic contract
    # ---------------------------------------------------------

    @abstractmethod
    def establish_designation(
        self,
        context,
    ) -> None:
        """
        Registers one grammatical designation.

        Concrete sūtras implement this.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Internal execution
    # ---------------------------------------------------------

    def _execute_rule(
        self,
        context,
    ) -> tuple:
        """
        Executes the designation semantics.
        """

        self.establish_designation(
            context,
        )

        return (context,)

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def designation_name(self) -> str:
        """
        Human-readable designation.

        Concrete subclasses may override.
        """
        return self.sutra_text

    def explain(self) -> str:
        return (
            f"Saṃjñā Sūtra : "
            f"{self.sutra_number}"
            " — "
            f"{self.designation_name}"
        )

    def trace(self) -> dict:

        trace = super().trace()

        trace.update(
            {
                "designation": self.designation_name,
            }
        )

        return trace
