"""
Unit Tests

Paninian Conflict Resolution Pipeline
"""

from SanskritAI.tests.panini.testing.panini_test_case import (
    PaninianTestCase,
)

from SanskritAI.domain.panini.paninian_rule_conflict import (
    PaninianRuleConflict,
)

from SanskritAI.domain.panini.paninian_default_conflict_pipeline import (
    DefaultPaninianConflictPipeline,
)


class TestConflictPipeline(PaninianTestCase):

    def test_pipeline_exists(self):

        pipeline = DefaultPaninianConflictPipeline()

        self.assert_true(
            pipeline.resolver_count >= 3
        )

    def test_pipeline_returns_one_rule(self):

        context = self.create_context()

        rule1 = self.create_rule()
        rule2 = self.create_rule()

        conflict = PaninianRuleConflict(
            context=context,
            candidate_rules=(
                rule1,
                rule2,
            ),
        )

        resolved = (
            pipeline := DefaultPaninianConflictPipeline()
        ).get_pipeline().resolve(conflict)

        self.assert_equal(
            len(resolved),
            1,
        )

    def test_empty_conflict(self):

        context = self.create_context()

        conflict = PaninianRuleConflict(
            context=context,
            candidate_rules=(),
        )

        resolved = (
            DefaultPaninianConflictPipeline()
            .get_pipeline()
            .resolve(conflict)
        )

        self.assert_equal(
            len(resolved),
            0,
        )
