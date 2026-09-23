from __future__ import annotations

"""
SanskritAI
==========

Abstract Saṃjñā Sūtra

Provides the canonical base class for every executable
Saṃjñā sūtra of the Aṣṭādhyāyī.

Purpose
-------

Nearly every Saṃjñā sūtra differs only in

    • the PaninianSutra
    • the designation it establishes
    • the execution logic

Everything else (classification, tracing,
metadata construction, diagnostics, etc.) is identical.

This class removes that duplication.

Architecture
------------

                    PaninianRule
                           │
                           ▼
                      SamjnaRule
                           │
                           ▼
                 AbstractSamjnaSutra
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   1.1.1               1.1.2              1.1.3
 vṛddhirādaic        adeṅ guṇaḥ      iko guṇavṛddhī

Responsibilities
----------------

• Builds immutable PaninianRuleMetadata

• Builds immutable PaninianSutra

• Standardises tracing

• Standardises diagnostics

• Allows subclasses to implement only
  the actual grammatical behaviour.

Future
------

Later this class will automatically integrate with

• PaninianRuleEngine

• Derivation Trace

• Knowledge Graph

• Commentary System

• Explainable AI

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.domain.panini.paninian_rule_category import (
    PaninianRuleCategory,
)
from SanskritAI.domain.panini.paninian_rule_metadata import (
    PaninianRuleMetadata,
)
from SanskritAI.domain.panini.paninian_rule_operation import (
    PaninianRuleOperation,
)
from SanskritAI.domain.panini.paninian_rule_priority import (
    PaninianRulePriority,
)
from SanskritAI.domain.panini.paninian_rule_type import (
    PaninianRuleType,
)
from SanskritAI.domain.panini.paninian_sutra import (
    PaninianSutra,
)
from SanskritAI.domain.panini.rules.samjna_rule import (
    SamjnaRule,
)


class AbstractSamjnaSutra(
    SamjnaRule,
    ABC,
):
    """
    Canonical base class for executable Saṃjñā sūtras.
    """

    def __init__(
        self,
        *,
        sutra: PaninianSutra,
        priority: PaninianRulePriority = (
            PaninianRulePriority.HIGHEST
        ),
        notes: str = "",
        tags: tuple[str, ...] = (),
        source: str = "Aṣṭādhyāyī",
    ) -> None:

        metadata = PaninianRuleMetadata(
            sutra=sutra,
            category=PaninianRuleCategory.SAMJNA,
            operation=PaninianRuleOperation.NONE,
            rule_type=PaninianRuleType.DEFINITION,
            priority=priority,
            source=source,
            notes=notes,
            tags=tags,
        )

        super().__init__(
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Standard applicability
    # ---------------------------------------------------------

    def supports(
        self,
        context,
    ) -> bool:
        """
        Saṃjñā rules are generally always applicable.

        Individual sūtras may override this.
        """
        return True

    # ---------------------------------------------------------
    # Execution contract
    # ---------------------------------------------------------

    @abstractmethod
    def establish_designation(
        self,
        context,
    ) -> None:
        """
        Establishes the grammatical designation.

        Concrete subclasses implement the
        actual Paninian semantics.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Standard execution wrapper
    # ---------------------------------------------------------

    def apply(
        self,
        context,
    ):
        """
        Executes the Saṃjñā sūtra.

        The default implementation delegates the
        grammatical work to establish_designation().
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
        Optional human-readable designation.

        Subclasses may override.
        """
        return self.metadata.sutra.sutra_text

    def explain(self) -> str:
        return (
            f"Saṃjñā Sūtra : "
            f"{self.metadata.sutra.sutra_number} — "
            f"{self.designation_name}"
        )

    def trace(self) -> dict:
        """
        Structured execution trace.
        """

        trace = super().trace()

        trace.update(
            {
                "sutra_number": self.metadata.sutra.sutra_number,
                "sutra_text": self.metadata.sutra.sutra_text,
                "designation": self.designation_name,
            }
        )

        return trace
