from __future__ import annotations

"""
SanskritAI
==========

Abstract Saṃjñā Sūtra

Canonical base class for all executable Saṃjñā sūtras.

Examples

    1.1.1  vṛddhir ādaic

    1.1.2  adeṅ guṇaḥ

    1.1.3  iko guṇavṛddhī

Responsibilities
----------------

• Inherits all canonical behaviour from AbstractSutra.

• Standardises the execution of grammatical
  designations (saṃjñā).

• Leaves only the actual designation logic to
  concrete sūtras.
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
        Saṃjñā sūtras are generally always applicable.

        Individual sūtras may override.
        """
        return self.is_enabled

    # ---------------------------------------------------------
    # Saṃjñā semantics
    # ---------------------------------------------------------

    @abstractmethod
    def establish_designation(
        self,
        context,
    ) -> None:
        """
        Registers the grammatical designation.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        context,
    ):
        """
        Executes the Saṃjñā semantics.
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
