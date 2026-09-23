from __future__ import annotations

"""
SanskritAI
==========

Default Reasoner

Canonical reasoning engine.

The DefaultReasoner coordinates the reasoning workflow and
delegates inference to the configured AI infrastructure.

Version
-------
v1.0.0
"""

from SanskritAI.ai.inference_result import InferenceResult
from SanskritAI.ai.reasoner import Reasoner
from SanskritAI.ai.reasoning_context import ReasoningContext


class DefaultReasoner(
    Reasoner,
):
    """
    Default implementation of the Reasoner.
    """

    def __init__(self, inference_engine):
        """
        Parameters
        ----------
        inference_engine:
            An object capable of performing AI inference.
            It is expected to expose:

                infer(context: ReasoningContext)
                    -> InferenceResult
        """
        self._inference_engine = inference_engine

    @property
    def inference_engine(self):
        return self._inference_engine

    def reason(
        self,
        context: ReasoningContext,
    ) -> InferenceResult:
        """
        Coordinates one reasoning session.
        """

        #
        # Future responsibilities may include:
        #
        # - Prompt preparation
        # - Memory injection
        # - Retrieval augmentation (RAG)
        # - Tool invocation
        # - Conversation trimming
        # - Reasoning telemetry
        # - Event publication
        #

        return self.inference_engine.infer(context)
