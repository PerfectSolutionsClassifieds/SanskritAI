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

    Uses the real AbstractSutra constructor so the
    test fixture remains compatible with the canonical
    Paninian rule hierarchy.
    """

    def __init__(self) -> None:
        super().__init__(
            metadata=self.metadata,
        )

    @property
    def metadata(
        self,
    ):
        return PaninianRuleMetadata(
            rule_name="MockRule",
            sutra_number="0.0.0",
            sutra_text="mock",
            operation=PaninianRuleOperation.NONE,
            behaviour=PaninianRuleBehaviour.TRANSFORMATION,
            adhyaya=0,
            pada=0,
        )

    def supports(
        self,
        context,
    ):
        return True

    def perform_transformation(
        self,
        context,
    ):
        """
        Minimal transformation used by the test fixture.

        The mock rule intentionally leaves the semantic
        subject unchanged while allowing the real
        Paninian execution hierarchy to operate.
        """

        return context


    def execute(
        self,
        context,
    ):
        """
        Execute the minimal mock transformation.
        """

        transformed = self.perform_transformation(
            context,
        )

        return (
            transformed.next_iteration(),
        )
