"""
Unit Tests

Execution Trace
"""

from SanskritAI.tests.panini.testing.panini_test_case import (
    PaninianTestCase,
)

from SanskritAI.domain.panini.paninian_execution_step import (
    PaninianExecutionStep,
)

from SanskritAI.domain.panini.paninian_execution_trace import (
    PaninianExecutionTrace,
)


class TestExecutionTrace(PaninianTestCase):

    def test_empty_trace(self):

        trace = PaninianExecutionTrace()

        self.assert_true(trace.is_empty)

        self.assert_trace_length(
            trace,
            0,
        )

    def test_append_step(self):

        context = self.create_context()

        rule = self.create_rule()

        step = PaninianExecutionStep(
            before=context,
            after=context.next_iteration(),
            rule=rule,
        )

        trace = PaninianExecutionTrace()

        trace = trace.append(step)

        self.assert_trace_length(
            trace,
            1,
        )

        self.assert_equal(
            trace.last_step.rule.sutra_number,
            "0.0.0",
        )

    def test_iteration(self):

        trace = PaninianExecutionTrace()

        self.assert_equal(
            len(tuple(trace)),
            0,
        )
