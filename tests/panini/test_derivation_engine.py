"""
Unit Tests

Paninian Derivation Engine
"""

from SanskritAI.tests.panini.testing.panini_test_case import (
    PaninianTestCase,
)


class TestDerivationEngine(PaninianTestCase):

    def test_engine_creation(self):

        engine = self.create_engine()

        self.assert_true(
            engine is not None
        )

    def test_empty_trace_on_creation(self):

        engine = self.create_engine()

        self.assert_trace_length(
            engine.execution_trace,
            0,
        )

    def test_context_creation(self):

        context = self.create_context()

        self.assert_context_iteration(
            context,
            0,
        )

    def test_engine_summary(self):

        engine = self.create_engine()

        summary = engine.summary()

        self.assert_true(
            "catalog_size" in summary
        )

        self.assert_true(
            "pipeline" in summary
        )

    def test_clear_trace(self):

        engine = self.create_engine()

        engine.clear_trace()

        self.assert_trace_length(
            engine.execution_trace,
            0,
        )
