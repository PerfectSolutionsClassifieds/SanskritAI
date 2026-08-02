from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Behaviour

Defines the canonical execution behaviour of a
Paninian grammatical rule.

Purpose
-------

Where

    PaninianRuleCategory

describes the classical grammatical classification,

and

    PaninianRuleOperation

describes *what* grammatical operation occurs,

PaninianRuleBehaviour describes *how* the rule
participates in the derivation engine.

This abstraction allows the execution engine to
reason about rules independently of their concrete
Python implementation.

Examples
--------

Saṃjñā
    establishes a grammatical designation

Vidhi
    performs a grammatical transformation

Niyama
    restricts an otherwise valid transformation

Atideśa
    extends an existing transformation

Paribhāṣā
    modifies interpretation of other rules

Adhikāra
    establishes grammatical scope

Future
------

The Rule Engine may dispatch different execution
strategies according to this behaviour.

Version
-------
v1.0.0
"""

from enum import Enum
from enum import unique


@unique
class PaninianRuleBehaviour(str, Enum):
    """
    Canonical execution behaviour of a Paninian rule.
    """

    # ---------------------------------------------------------
    # Definition
    # ---------------------------------------------------------

    DESIGNATION = "designation"

    # ---------------------------------------------------------
    # Direct grammatical action
    # ---------------------------------------------------------

    TRANSFORMATION = "transformation"

    # ---------------------------------------------------------
    # Restricts another rule
    # ---------------------------------------------------------

    RESTRICTION = "restriction"

    # ---------------------------------------------------------
    # Extends another rule
    # ---------------------------------------------------------

    EXTENSION = "extension"

    # ---------------------------------------------------------
    # Governs interpretation
    # ---------------------------------------------------------

    INTERPRETATION = "interpretation"

    # ---------------------------------------------------------
    # Establishes grammatical scope
    # ---------------------------------------------------------

    SCOPE = "scope"

    # ---------------------------------------------------------
    # Pure organizational / informational
    # ---------------------------------------------------------

    ORGANIZATIONAL = "organizational"

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.value.replace("_", " ").title()

    @property
    def is_transformative(self) -> bool:
        return self in {
            PaninianRuleBehaviour.TRANSFORMATION,
            PaninianRuleBehaviour.EXTENSION,
        }

    @property
    def is_contextual(self) -> bool:
        return self in {
            PaninianRuleBehaviour.INTERPRETATION,
            PaninianRuleBehaviour.SCOPE,
            PaninianRuleBehaviour.RESTRICTION,
        }

    @property
    def is_descriptive(self) -> bool:
        return self is PaninianRuleBehaviour.DESIGNATION
