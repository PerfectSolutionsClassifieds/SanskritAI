from __future__ import annotations

"""
SanskritAI
==========

Abstract Sūtra

The canonical base class for every executable sūtra of the
Aṣṭādhyāyī.

Purpose
-------

This class encapsulates everything common to ALL Paninian
sūtras, regardless of their grammatical category.

Every executable sūtra ultimately derives from this class.

Architecture
------------

                        PaninianRule
                              │
                              ▼
                       AbstractSutra
                              │
        ┌─────────────┬────────┴────────┬─────────────┐
        ▼             ▼                 ▼             ▼
AbstractSamjna  AbstractVidhi   AbstractParibhasha  ...
      │               │
      ▼               ▼
 1.1.1             6.1.77
 1.1.2             6.1.87

Responsibilities
----------------

• Owns the canonical PaninianSutra.

• Owns immutable PaninianRuleMetadata.

• Standardizes tracing.

• Standardizes diagnostics.

• Standardizes applicability.

• Standardizes execution lifecycle.

Future
------

Later this class will integrate with

• Rule Engine

• Derivation Trace

• Knowledge Graph

• Commentary System

• Explainable AI

• Versioned Grammar Repository

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.domain.panini.paninian_rule import PaninianRule
from SanskritAI.domain.panini.paninian_rule_metadata import (
    PaninianRuleMetadata,
)
from SanskritAI.domain.panini.paninian_sutra import (
    PaninianSutra,
)


class AbstractSutra(
    PaninianRule,
    ABC,
):
    """
    Canonical executable Paninian sūtra.
    """

    def __init__(
        self,
        *,
        metadata: PaninianRuleMetadata,
    ) -> None:
        """
        Every executable sūtra owns exactly one immutable
        metadata object.
        """
        super().__init__(
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Canonical Sutra
    # ---------------------------------------------------------

    @property
    def sutra(self) -> PaninianSutra:
        """
        Returns the immutable canonical sūtra.
        """
        return self.metadata.sutra

    @property
    def sutra_number(self) -> str:
        return self.sutra.sutra_number

    @property
    def sutra_text(self) -> str:
        return self.sutra.sutra_text

    @property
    def transliteration(self) -> str:
        return self.sutra.transliteration

    @property
    def translation(self) -> str:
        return self.sutra.translation

    @property
    def canonical_location(self) -> str:
        return self.sutra.canonical_location

    # ---------------------------------------------------------
    # Applicability
    # ---------------------------------------------------------

    def supports(
        self,
        context,
    ) -> bool:
        """
        Default implementation.

        Concrete subclasses may override.
        """
        return self.is_enabled

    # ---------------------------------------------------------
    # Life-cycle
    # ---------------------------------------------------------

    def before_apply(
        self,
        context,
    ):
        """
        Hook before execution.
        """
        return context

    @abstractmethod
    def execute(
        self,
        context,
    ) -> tuple:
        """
        Executes the actual grammatical semantics.

        Concrete subclasses implement this.
        """
        raise NotImplementedError

    def apply(
        self,
        context,
    ) -> tuple:
        """
        Canonical execution wrapper.

        Every executable sūtra follows this lifecycle.

            before_apply()

            execute()

            after_apply()
        """

        context = self.before_apply(
            context,
        )

        result = self.execute(
            context,
        )

        result = self.after_apply(
            context,
            result,
        )

        return result

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def explain(self) -> str:
        """
        Human-readable explanation.
        """
        return (
            f"{self.sutra_number}"
            " — "
            f"{self.translation}"
        )

    def trace(self) -> dict:
        """
        Canonical trace payload.

        Every executable sūtra automatically contributes
        identical trace information.
        """

        trace = super().trace()

        trace.update(
            {
                "sutra_number": self.sutra_number,
                "sutra_text": self.sutra_text,
                "transliteration": self.transliteration,
                "translation": self.translation,
                "canonical_location": self.canonical_location,
            }
        )

        return trace

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.sutra_number

    @property
    def display_text(self) -> str:
        return (
            f"{self.sutra_number}"
            " — "
            f"{self.sutra_text}"
        )

    @property
    def display_description(self) -> str:
        return self.translation

    def __str__(self) -> str:
        return self.display_text
