from __future__ import annotations

"""
SanskritAI
==========

Agent

Defines the abstract AI Agent.

An Agent coordinates reasoning and tool invocation while
delegating its execution policy to an AgentStrategy.

Architecture
------------

KnowledgeContext
        │
        ▼
Agent
        │
        ├── AgentStrategy
        ├── Reasoner
        └── Tool(s)

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.ai.agent_strategy import AgentStrategy
from SanskritAI.ai.knowledge_context import KnowledgeContext
from SanskritAI.ai.reasoner import Reasoner
from SanskritAI.ai.tool import Tool
from SanskritAI.core.mixins.displayable import Displayable


class Agent(
    ABC,
    Displayable,
):
    """
    Abstract AI Agent.

    Coordinates one complete intelligent session while
    delegating execution policy to an AgentStrategy.
    """

    def __init__(
        self,
        strategy: AgentStrategy,
        reasoner: Reasoner,
        tools: tuple[Tool, ...] = (),
    ):
        self._strategy = strategy
        self._reasoner = reasoner
        self._tools = tools

    @property
    def strategy(self) -> AgentStrategy:
        """
        Configured execution strategy.
        """
        return self._strategy

    @property
    def reasoner(self) -> Reasoner:
        """
        Configured reasoning engine.
        """
        return self._reasoner

    @property
    def tools(self) -> tuple[Tool, ...]:
        """
        Available tools.
        """
        return self._tools

    @property
    def tool_count(self) -> int:
        return len(self._tools)

    @property
    def has_tools(self) -> bool:
        return self.tool_count > 0

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract AI agent."

    @abstractmethod
    def execute(
        self,
        context: KnowledgeContext,
    ) -> object:
        """
        Executes one complete intelligent session.
        """
        raise NotImplementedError
