from __future__ import annotations

"""
SanskritAI

Mock Derivation Context

Factory for creating valid immutable
PaninianDerivationContext objects.
"""

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)

from SanskritAI.tests.panini.mocks.mock_subject import (
    MockSubject,
)


def create_mock_context(
    text: str = "अ",
) -> PaninianDerivationContext:
    """
    Returns a valid derivation context.
    """

    return PaninianDerivationContext(
        subject=MockSubject(text=text),
        derivation_id="mock-1",
        stage="unit-test",
        description="Mock derivation context",
    )
