from __future__ import annotations

"""
SanskritAI
==========

Default Agent

Canonical Agent implementation.

Coordinates one complete agent session by delegating the
execution policy to the configured AgentStrategy.

Architecture
------------

KnowledgeContext
        │
        ▼
Agent
        │
        ▼
AgentStrategy

Version
-------
v1.0.0
"""

from SanskritAI.ai.agent import Agent
from SanskritAI.ai.knowledge_context import KnowledgeContext


class DefaultAgent(
    Agent,
):
    """
    Canonical Agent implementation.
    """

    def __init__(
        self,
        strategy,
        reasoner,
        tools=(),
    ):
        super().__init__(
            reasoner=reasoner,
            tools=tools,
        )
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    def execute(
        self,
        context: KnowledgeContext,
    ):
        """
        Coordinates one complete agent session.

        Future responsibilities may include:

        • Event publication
        • Diagnostics
        • Telemetry
        • Tool scheduling
        • Multi-agent coordination
        • Tracing
        """

        return self.strategy.execute(context)
