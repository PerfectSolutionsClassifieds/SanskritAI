from __future__ import annotations

"""
SanskritAI
==========

Default Reasoner

Canonical reasoning coordinator.

Coordinates the reasoning lifecycle and delegates the
reasoning policy to the configured ReasoningStrategy.
"""

from SanskritAI.ai.inference_result import InferenceResult
from SanskritAI.ai.reasoner import Reasoner
from SanskritAI.ai.reasoning_context import ReasoningContext


class DefaultReasoner(
    Reasoner,
):
    """
    Canonical Reasoner implementation.
    """

    def reason(
        self,
        context: ReasoningContext,
    ) -> InferenceResult:

        #
        # Future responsibilities:
        #
        # • Event publication
        # • Telemetry
        # • Diagnostics
        # • Timing
        # • Tracing
        #

        return self.strategy.reason(context)
