from __future__ import annotations

"""
SanskritAI
==========

Default Paninian Rule Matcher

Canonical implementation of the PaninianRuleMatcher.

Responsibilities
----------------

Evaluates one rule in the following order:

    1. Rule enabled?
    2. Rule.supports(context)
    3. Rule.validate(context)
    4. Every RuleCondition
    5. Produce PaninianRuleMatchResult

The matcher intentionally performs NO grammatical
transformation.

Its sole responsibility is determining applicability.

Version
-------
v1.1.0
"""

from dataclasses import dataclass
from typing import Any

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)

from SanskritAI.domain.panini.paninian_rule_condition import (
    PaninianRuleCondition,
)

from SanskritAI.domain.panini.paninian_rule_match_result import (
    PaninianRuleMatchResult,
)

from SanskritAI.domain.panini.paninian_rule_matcher import (
    PaninianRuleMatcher,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultPaninianRuleMatcher(
    PaninianRuleMatcher,
):
    """
    Canonical Paninian rule matcher.

    The public contract is:

        match(rule, context)

    One rule is evaluated at a time.
    """

    # ---------------------------------------------------------
    # Matching
    # ---------------------------------------------------------

    def match(
        self,
        rule: PaninianRule,
        context: Any,
    ) -> PaninianRuleMatchResult:
        """
        Evaluates one Paninian rule against the
        supplied derivation context.
        """

        diagnostics: list[str] = []

        matched_conditions: list[str] = []

        failed_conditions: list[str] = []

        # -----------------------------------------------------
        # Enabled
        # -----------------------------------------------------

        if not rule.is_enabled:

            diagnostics.append(
                "Rule disabled.",
            )

            return PaninianRuleMatchResult(
                rule=rule,
                matched=False,
                score=0.0,
                confidence=1.0,
                matched_conditions=(),
                failed_conditions=(
                    "enabled",
                ),
                diagnostics=tuple(
                    diagnostics,
                ),
            )

        # -----------------------------------------------------
        # supports()
        # -----------------------------------------------------

        if not rule.supports(
            context,
        ):

            diagnostics.append(
                "supports(context) returned False.",
            )

            return PaninianRuleMatchResult(
                rule=rule,
                matched=False,
                score=0.0,
                confidence=1.0,
                matched_conditions=(),
                failed_conditions=(
                    "supports",
                ),
                diagnostics=tuple(
                    diagnostics,
                ),
            )

        matched_conditions.append(
            "supports",
        )

        # -----------------------------------------------------
        # validate()
        # -----------------------------------------------------

        if not rule.validate(
            context,
        ):

            diagnostics.append(
                "validate(context) returned False.",
            )

            return PaninianRuleMatchResult(
                rule=rule,
                matched=False,
                score=0.0,
                confidence=1.0,
                matched_conditions=tuple(
                    matched_conditions,
                ),
                failed_conditions=(
                    "validate",
                ),
                diagnostics=tuple(
                    diagnostics,
                ),
            )

        matched_conditions.append(
            "validate",
        )

        # -----------------------------------------------------
        # Rule Conditions
        # -----------------------------------------------------

        conditions = getattr(
            rule,
            "conditions",
            (),
        )

        for condition in conditions:

            if not isinstance(
                condition,
                PaninianRuleCondition,
            ):

                diagnostics.append(
                    "Ignoring invalid condition "
                    f"{condition!r}.",
                )

                continue

            if condition.evaluate(
                context,
            ):

                matched_conditions.append(
                    condition.name,
                )

            else:

                failed_conditions.append(
                    condition.name,
                )

        # -----------------------------------------------------
        # Final Decision
        # -----------------------------------------------------

        matched = (
            len(
                failed_conditions,
            )
            == 0
        )

        total_conditions = (
            len(
                matched_conditions,
            )
            + len(
                failed_conditions,
            )
        )

        if total_conditions == 0:

            score = 1.0

        else:

            score = (
                len(
                    matched_conditions,
                )
                / total_conditions
            )

        confidence = score

        if matched:

            diagnostics.append(
                "Rule successfully matched.",
            )

        else:

            diagnostics.append(
                "One or more conditions failed.",
            )

        return PaninianRuleMatchResult(
            rule=rule,
            matched=matched,
            score=score,
            confidence=confidence,
            matched_conditions=tuple(
                matched_conditions,
            ),
            failed_conditions=tuple(
                failed_conditions,
            ),
            diagnostics=tuple(
                diagnostics,
            ),
        )
