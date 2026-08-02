from __future__ import annotations

"""
SanskritAI
==========

Paninian Test Utility

Reusable helper for Paninian unit tests.

Purpose
-------

Provides common construction helpers for

    • Mock derivation contexts

    • Mock executable rules

    • Derivation engine

    • Assertions

Every Paninian sūtra test should reuse this class.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.panini.paninian_derivation_engine import (
    PaninianDerivationEngine,
)

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)

from SanskritAI.domain.panini.paninian_execution_trace import (
    PaninianExecutionTrace,
)

from SanskritAI.tests.panini.mocks.mock_derivation_context import (
    create_mock_context,
)

from SanskritAI.tests.panini.mocks.mock_rule import (
    MockRule,
)


@dataclass(slots=True)
class PaninianTestCase:
    """
    Reusable testing utility.
    """

    # ---------------------------------------------------------
    # Builders
    # ---------------------------------------------------------

    def create_context(
        self,
        text: str = "अ",
    ) -> PaninianDerivationContext:
        """
        Creates a valid derivation context.
        """

        return create_mock_context(
            text=text,
        )

    def create_rule(
        self,
    ) -> MockRule:
        """
        Creates a mock executable rule.
        """

        return MockRule()

    def create_engine(
        self,
    ) -> PaninianDerivationEngine:
        """
        Creates a fresh derivation engine.
        """

        return PaninianDerivationEngine()

    # ---------------------------------------------------------
    # Assertions
    # ---------------------------------------------------------

    def assert_true(
        self,
        condition: bool,
        message: str = "",
    ) -> None:
        """
        Boolean assertion.
        """

        if not condition:
            raise AssertionError(
                message or "Expected True."
            )

    def assert_false(
        self,
        condition: bool,
        message: str = "",
    ) -> None:
        """
        Boolean assertion.
        """

        if condition:
            raise AssertionError(
                message or "Expected False."
            )

    def assert_equal(
        self,
        actual,
        expected,
        message: str = "",
    ) -> None:
        """
        Equality assertion.
        """

        if actual != expected:
            raise AssertionError(
                message
                or f"{actual!r} != {expected!r}"
            )

    def assert_trace_length(
        self,
        trace: PaninianExecutionTrace,
        expected: int,
    ) -> None:
        """
        Verifies execution trace size.
        """

        self.assert_equal(
            trace.step_count,
            expected,
            "Unexpected trace length.",
        )

    def assert_context_iteration(
        self,
        context: PaninianDerivationContext,
        expected: int,
    ) -> None:
        """
        Verifies derivation iteration.
        """

        self.assert_equal(
            context.iteration,
            expected,
            "Unexpected iteration.",
        )

    def assert_rule_applied(
        self,
        trace: PaninianExecutionTrace,
        sutra_number: str,
    ) -> None:
        """
        Verifies that a sutra appears in
        the execution trace.
        """

        found = any(
            step.rule.sutra_number == sutra_number
            for step in trace
        )

        self.assert_true(
            found,
            f"Sūtra {sutra_number} was not executed.",
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def print_trace(
        self,
        trace: PaninianExecutionTrace,
    ) -> None:
        """
        Pretty-prints the execution trace.
        """

        for index, step in enumerate(trace, start=1):

            print(
                f"{index:02d}. "
                f"{step.rule.sutra_number} "
                f"{step.rule.sutra}"
            )
