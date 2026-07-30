from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Type

Defines the behavioral semantics of a Paninian rule.

Unlike PaninianRuleCategory, which answers

    "What grammatical family does this rule belong to?"

PaninianRuleType answers

    "How should this rule behave during derivation?"

A rule's type determines its execution semantics,
interaction with other rules, and participation in
conflict resolution.

Examples
--------

Category:
    Sandhi

Type:
    Mandatory

Category:
    Lopa

Type:
    Optional

Category:
    Samjna

Type:
    Annotation

These are orthogonal concepts.

Version
-------
v1.0.0
"""

from enum import Enum
from enum import unique


@unique
class PaninianRuleType(str, Enum):
    """
    Behavioral classification of Paninian rules.
    """

    # ---------------------------------------------------------
    # Execution Semantics
    # ---------------------------------------------------------

    MANDATORY = "mandatory"
    OPTIONAL = "optional"

    # ---------------------------------------------------------
    # Classical Paninian Behaviour
    # ---------------------------------------------------------

    UTSARGA = "utsarga"
    APAVADA = "apavada"
    NIYAMA = "niyama"
    VIKALPA = "vikalpa"
    ATIDESHA = "atidesha"

    # ---------------------------------------------------------
    # Informational
    # ---------------------------------------------------------

    ANNOTATION = "annotation"
    VALIDATION = "validation"

    # ---------------------------------------------------------
    # Infrastructure
    # ---------------------------------------------------------

    PREPARATION = "preparation"
    TRANSFORMATION = "transformation"
    FINALIZATION = "finalization"

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return {
            self.MANDATORY: "Mandatory",
            self.OPTIONAL: "Optional",

            self.UTSARGA: "Utsarga",
            self.APAVADA: "Apavāda",
            self.NIYAMA: "Niyama",
            self.VIKALPA: "Vikalpa",
            self.ATIDESHA: "Atideśa",

            self.ANNOTATION: "Annotation",
            self.VALIDATION: "Validation",

            self.PREPARATION: "Preparation",
            self.TRANSFORMATION: "Transformation",
            self.FINALIZATION: "Finalization",
        }[self]

    # ---------------------------------------------------------
    # Classification Helpers
    # ---------------------------------------------------------

    @property
    def is_executable(self) -> bool:
        """
        Returns True if the rule actively transforms
        the derivation.
        """
        return self in {
            self.MANDATORY,
            self.OPTIONAL,
            self.UTSARGA,
            self.APAVADA,
            self.NIYAMA,
            self.VIKALPA,
            self.ATIDESHA,
            self.TRANSFORMATION,
        }

    @property
    def is_annotation(self) -> bool:
        """
        Returns True if the rule only annotates the
        derivation without changing the form.
        """
        return self is self.ANNOTATION

    @property
    def is_validation(self) -> bool:
        """
        Returns True if the rule validates state.
        """
        return self is self.VALIDATION

    @property
    def is_optional(self) -> bool:
        """
        Returns True if application is optional.
        """
        return self in {
            self.OPTIONAL,
            self.VIKALPA,
        }

    @property
    def is_exception(self) -> bool:
        """
        Returns True if this rule overrides another
        rule (Apavāda).
        """
        return self is self.APAVADA

    @property
    def is_default(self) -> bool:
        """
        Returns True if this rule represents an
        Utsarga (default rule).
        """
        return self is self.UTSARGA

    def __str__(self) -> str:
        return self.display_name
