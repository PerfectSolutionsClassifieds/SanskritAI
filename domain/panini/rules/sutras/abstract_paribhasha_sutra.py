from __future__ import annotations

"""
SanskritAI
==========

Abstract Paribhāṣā Sūtra

Canonical executable base class for every
Paribhāṣā (meta-rule) of the Aṣṭādhyāyī.

Examples
--------

1.1.56   स्थानिवदादेशोऽनल्विधौ

Purpose
-------

A Paribhāṣā Sūtra governs the interpretation,
precedence, applicability, or interaction of
other grammatical rules.

Unlike Vidhi Sūtras, Paribhāṣā Sūtras usually
do not perform direct linguistic transformations.
Instead, they modify how the rule engine behaves.

Responsibilities
----------------

• inherits the canonical execution life-cycle

• modifies rule interpretation

• influences rule precedence

• influences applicability

• records meta-rule trace

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.domain.panini.rules.sutras.abstract_sutra import (
    AbstractSutra,
)


class AbstractParibhashaSutra(
    AbstractSutra,
    ABC,
):
    """
    Canonical executable Paribhāṣā Sūtra.
    """

    # ---------------------------------------------------------
    # Applicability
    # ---------------------------------------------------------

    def supports(
        self,
        context,
    ) -> bool:
        """
        Meta-rules are normally globally applicable.

        Concrete sūtras may override.
        """
        return self.is_enabled

    # ---------------------------------------------------------
    # Semantic contract
    # ---------------------------------------------------------

    @abstractmethod
    def apply_meta_rule(
        self,
        context,
    ):
        """
        Applies the grammatical meta-rule.

        Concrete subclasses implement the
        interpretation logic.
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
        Executes the Paribhāṣā semantics.
        """

        result = self.apply_meta_rule(
            context,
        )

        if result is None:
            result = context

        return (result,)

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def meta_rule_name(self) -> str:
        """
        Human-readable meta-rule name.
        """
        return self.sutra_text

    def explain(self) -> str:
        return (
            f"Paribhāṣā Sūtra : "
            f"{self.sutra_number}"
            " — "
            f"{self.meta_rule_name}"
        )

    def trace(self) -> dict:
        """
        Structured execution trace.
        """

        trace = super().trace()

        trace.update(
            {
                "meta_rule": self.meta_rule_name,
            }
        )

        return trace
