from __future__ import annotations

"""
SanskritAI
==========

Default Agent

Canonical Agent implementation.

Coordinates one complete agent session by delegating its
execution policy to the configured AgentStrategy.

Architecture
------------

KnowledgeContext
        │
        ▼
DefaultAgent
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

    def execute(
        self,
        context: KnowledgeContext,
    ):
        """
        Coordinates one complete intelligent session.

        Future responsibilities may include:

        • Event publication
        • Diagnostics
        • Telemetry
        • Tracing
        • Session lifecycle management
        • Multi-agent coordination
        """

        return self.strategy.execute(context)
