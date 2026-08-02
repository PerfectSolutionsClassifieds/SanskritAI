from __future__ import annotations

"""
SanskritAI
==========

Abstract Vidhi Sūtra

Canonical executable base class for every Vidhi
(operative / prescriptive) sūtra of the
Aṣṭādhyāyī.

Examples
--------

6.1.77    iko yaṇ aci

7.3.84    sārvadhātukārdhadhātukayoḥ

3.1.68    kartari śap

Purpose
-------

A Vidhi Sūtra performs an actual grammatical
transformation.

Unlike Saṃjñā Sūtras, which establish technical
designations, Vidhi Sūtras modify the derivation.

Responsibilities
----------------

• inherits canonical execution life-cycle

• performs grammatical transformation

• records transformation trace

• allows subclasses to implement only the
  linguistic semantics

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.domain.panini.rules.sutras.abstract_sutra import (
    AbstractSutra,
)


class AbstractVidhiSutra(
    AbstractSutra,
    ABC,
):
    """
    Canonical executable Vidhi Sūtra.
    """

    # ---------------------------------------------------------
    # Applicability
    # ---------------------------------------------------------

    def supports(
        self,
        context,
    ) -> bool:
        """
        Vidhi rules are condition-dependent.

        Concrete sūtras almost always override this.
        """
        return self.is_enabled

    # ---------------------------------------------------------
    # Semantic contract
    # ---------------------------------------------------------

    @abstractmethod
    def perform_transformation(
        self,
        context,
    ):
        """
        Performs the grammatical transformation.

        Concrete sūtras implement the actual
        Paninian operation.
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
        Executes one Vidhi transformation.
        """

        result = self.perform_transformation(
            context,
        )

        if result is None:
            result = context

        return (result,)

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def transformation_name(self) -> str:
        """
        Human-readable transformation name.

        Concrete subclasses may override.
        """
        return self.sutra_text

    def explain(self) -> str:
        return (
            f"Vidhi Sūtra : "
            f"{self.sutra_number}"
            " — "
            f"{self.transformation_name}"
        )

    def trace(self) -> dict:

        trace = super().trace()

        trace.update(
            {
                "transformation": self.transformation_name,
            }
        )

        return trace
