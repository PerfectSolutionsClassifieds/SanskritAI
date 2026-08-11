from __future__ import annotations

"""
SanskritAI
==========

Mock Rule

Minimal executable rule used by Paninian unit tests.

The mock intentionally inherits the real Paninian
execution hierarchy so that the tests exercise the
canonical rule lifecycle rather than a parallel
test-only implementation.

Version
-------
v3.0.0
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

    The rule:

    • is always applicable
    • performs no semantic modification
    • returns the incoming context
    • relies on AbstractSutra for the canonical
      execution lifecycle
    """

    def __init__(self) -> None:
        super().__init__(
            metadata=self.metadata,
        )

    # ---------------------------------------------------------
    # Canonical Metadata
    # ---------------------------------------------------------

    @property
    def metadata(
        self,
    ) -> PaninianRuleMetadata:
        """
        Constructs canonical metadata for the mock rule.
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

        return PaninianRuleMetadata(
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

        The mock intentionally leaves the semantic
        subject unchanged.

        AbstractVidhiSutra wraps this method inside
        the canonical AbstractSutra lifecycle.
        """

        return context
