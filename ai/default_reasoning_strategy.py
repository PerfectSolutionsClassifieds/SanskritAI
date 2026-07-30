from __future__ import annotations

"""
SanskritAI
==========

Default Reasoning Strategy

Canonical reasoning policy.

Delegates reasoning to the configured inference engine.
"""

from SanskritAI.ai.inference_result import InferenceResult
from SanskritAI.ai.reasoning_context import ReasoningContext
from SanskritAI.ai.reasoning_strategy import ReasoningStrategy


class DefaultReasoningStrategy(
    ReasoningStrategy,
):
    """
    Default reasoning strategy.
    """

    def __init__(
        self,
        inference_engine,
    ):
        self._inference_engine = inference_engine

    @property
    def inference_engine(self):
        return self._inference_engine

    def reason(
        self,
        context: ReasoningContext,
    ) -> InferenceResult:

        #
        # Future extensions:
        #
        # • Prompt optimization
        # • Memory augmentation
        # • RAG
        # • Tool invocation
        # • Chain-of-thought orchestration
        # • Multi-agent coordination
        #

        return self.inference_engine.infer(context)
