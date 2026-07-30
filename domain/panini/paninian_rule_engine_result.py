from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Engine Result

Canonical output produced by the Paninian Rule Engine.

Every Paninian derivation stage receives this object after the
Rule Engine has completed execution.

Rather than exposing internal engine behaviour, the Rule Engine
returns one immutable result describing

    • resulting form
    • evaluated rules
    • matched rules
    • applied rules
    • transformation count

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable


@dataclass(slots=True)
class PaninianRuleEngineResult(Displayable):
    """
    Canonical output of PaninianRuleEngine.
    """

    resulting_form: str = ""

    evaluated_rules: tuple[str, ...] = ()

    matched_rules: tuple[str, ...] = ()

    applied_rules: tuple[str, ...] = ()

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Rule Engine Result"

    @property
    def display_description(self) -> str:
        return (
            "Result produced by the Paninian Rule Engine."
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def evaluated_rule_count(self) -> int:
        return len(self.evaluated_rules)

    @property
    def matched_rule_count(self) -> int:
        return len(self.matched_rules)

    @property
    def applied_rule_count(self) -> int:
        return len(self.applied_rules)

    @property
    def changed(self) -> bool:
        return self.applied_rule_count > 0

    @property
    def has_matches(self) -> bool:
        return self.matched_rule_count > 0

    @property
    def has_applications(self) -> bool:
        return self.applied_rule_count > 0

    # ---------------------------------------------------------

    def __bool__(self) -> bool:
        return self.has_applications

    def __str__(self) -> str:
        return (
            f"{self.display_name}"
            f"(applied={self.applied_rule_count})"
        )
