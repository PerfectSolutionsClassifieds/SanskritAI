
from __future__ import annotations

"""
SanskritAI
==========

Mock Rule

Minimal executable rule used by Paninian unit tests.

The mock inherits the real Paninian execution hierarchy
and therefore exercises the canonical rule lifecycle.

Version
-------
v4.0.0
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

from SanskritAI.domain.panini.paninian_rule_type import (
    PaninianRuleType,
)

from SanskritAI.domain.panini.paninian_rule_priority import (
    PaninianRulePriority,
)

from SanskritAI.domain.panini.paninian_rule_category import (
    PaninianRuleCategory,
)

from SanskritAI.domain.panini.paninian_sutra import (
    PaninianSutra,
)


class MockRule(
    AbstractVidhiSutra,
):
    """
    Minimal executable Paninian rule.

    The mock:

    • owns normal inherited metadata
    • is always applicable
    • performs no semantic modification
    • uses the real AbstractSutra lifecycle
    • implements only perform_transformation()
    """

    def __init__(self) -> None:
        """
        Construct the mock using the canonical
        PaninianRuleMetadata object.
        """

        sutra = PaninianSutra(
            identifier="mock-0.0.0",
            sutra_number="0.0.0",
            sutra_text="mock",
            transliteration="mock",
            translation="Mock Paninian rule",
            adhyaya=0,
            pada=0,
            source="SanskritAI Test Suite",
        )

        metadata = PaninianRuleMetadata(
            sutra=sutra,
            category=PaninianRuleCategory.ADESHA,
            operation=PaninianRuleOperation.NONE,
            rule_type=PaninianRuleType.MANDATORY,
            priority=PaninianRulePriority.NORMAL,
            source="SanskritAI Test Suite",
            notes="Minimal executable mock rule.",
            tags=(
                "test",
                "mock",
                "panini",
            ),
        )

        super().__init__(
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Applicability
    # ---------------------------------------------------------

    def supports(
        self,
        context,
    ) -> bool:
        """
        The mock rule is always applicable.
        """

        return True

    # ---------------------------------------------------------
    # Semantic Transformation
    # ---------------------------------------------------------

    def perform_transformation(
        self,
        context,
    ):
        """
        Minimal transformation used by the test fixture.

        The semantic subject remains unchanged.

        AbstractVidhiSutra._execute_rule() wraps the
        returned context into the canonical execution
        result tuple.
        """

        return context
