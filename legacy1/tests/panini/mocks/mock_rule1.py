from __future__ import annotations

"""
SanskritAI

Mock Rule

Simple executable rule used by unit tests.

It inherits the real Paninian hierarchy so that
the execution engine is tested without
modification.
"""

from SanskritAI.domain.panini.rules.sutras.abstract_vidhi_sutra import (
    AbstractVidhiSutra,
)

from SanskritAI.domain.panini.paninian_rule_metadata import (
    PaninianRuleMetadata,
)

from SanskritAI.domain.panini.paninian_rule_operation import (
    PaninianRuleOperation,
)

from SanskritAI.domain.panini.paninian_rule_behaviour import (
    PaninianRuleBehaviour,
)


class MockRule(
    AbstractVidhiSutra,
):
    """
    Minimal executable rule.
    """

    @property
    def metadata(
        self,
    ):
        return PaninianRuleMetadata(
            rule_name="MockRule",
            sutra_number="0.0.0",
            sutra_text="mock",
            operation=PaninianRuleOperation.VIDHI,
            behaviour=PaninianRuleBehaviour.MANDATORY,
            adhyaya=0,
            pada=0,
        )

    def supports(
        self,
        context,
    ):
        return True

    def execute(
        self,
        context,
    ):
        """
        Returns the incoming context unchanged.
        """

        return (context.next_iteration(),)
