"""
Integration Test

Aṣṭādhyāyī 1.1.1

वृद्धिरादैच्

This is the first end-to-end integration test of the
Paninian execution kernel.

The test validates

    • Catalog discovery

    • Rule matching

    • Conflict pipeline

    • Rule execution

    • Derivation context evolution

    • Execution trace generation
"""

from SanskritAI.tests.panini.testing.panini_test_case import (
    PaninianTestCase,
)

from SanskritAI.domain.panini.paninian_sutra_catalog import (
    PaninianSutraCatalog,
)


class TestVrddhirAdaic(PaninianTestCase):

    def test_sutra_exists_in_catalog(self):
        """
        The canonical sūtra must be discoverable.
        """

        catalog = PaninianSutraCatalog()

        sutra = catalog.get(
            "1.1.1",
        )

        self.assert_true(
            sutra is not None,
            "Sūtra 1.1.1 is not registered.",
        )

        self.assert_equal(
            sutra.sutra_number,
            "1.1.1",
        )

    def test_basic_derivation(self):
        """
        Executes one derivation cycle.
        """

        catalog = PaninianSutraCatalog()

        engine = self.create_engine()

        # ensure engine uses canonical catalog

        engine.catalog = catalog

        context = self.create_context(
            text="ऐ",
        )

        result = engine.derive(
            context,
        )

        # ------------------------------------
        # Result must remain a derivation context
        # ------------------------------------

        self.assert_true(
            result is not None,
        )

        # ------------------------------------
        # Trace must exist
        # ------------------------------------

        trace = engine.execution_trace

        self.assert_true(
            trace is not None,
        )

        # ------------------------------------
        # Engine summary should be available
        # ------------------------------------

        summary = engine.summary()

        self.assert_true(
            "pipeline" in summary,
        )

    def test_trace_contains_sutra(self):
        """
        The execution trace should record
        execution of 1.1.1.
        """

        catalog = PaninianSutraCatalog()

        engine = self.create_engine()

        engine.catalog = catalog

        context = self.create_context(
            text="ऐ",
        )

        engine.derive(
            context,
        )

        trace = engine.execution_trace

        if trace.step_count == 0:

            raise AssertionError(
                "No Paninian rule executed."
            )

        self.assert_rule_applied(
            trace,
            "1.1.1",
        )

    def test_pipeline_is_used(self):
        """
        Confirms the engine owns the canonical
        conflict-resolution pipeline.
        """

        engine = self.create_engine()

        self.assert_true(
            engine.conflict_pipeline
            is not None,
        )

        self.assert_true(
            engine.conflict_pipeline
            .resolver_count >= 3,
        )

    def test_engine_is_repeatable(self):
        """
        Running derivation twice should not
        corrupt execution state.
        """

        catalog = PaninianSutraCatalog()

        engine = self.create_engine()

        engine.catalog = catalog

        context = self.create_context(
            text="ऐ",
        )

        engine.derive(context)

        first_count = (
            engine.execution_trace.step_count
        )

        engine.clear_trace()

        engine.derive(context)

        second_count = (
            engine.execution_trace.step_count
        )

        self.assert_equal(
            first_count,
            second_count,
        )
