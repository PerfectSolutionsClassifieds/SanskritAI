from __future__ import annotations

"""
SanskritAI
==========

Agent

Defines the abstract AI Agent.

An Agent coordinates reasoning, knowledge, and tools to
perform higher-level intelligent tasks.

The Agent itself owns no concrete reasoning or tool
implementation; instead, it delegates to the configured
Reasoner and Tool instances.

Architecture
------------

KnowledgeContext
        │
        ▼
Agent
        │
        ├── Reasoner
        └── Tool(s)

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

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
    """

    def __init__(
        self,
        reasoner: Reasoner,
        tools: tuple[Tool, ...] = (),
    ):
        self._reasoner = reasoner
        self._tools = tools

    @property
    def reasoner(self) -> Reasoner:
        return self._reasoner

    @property
    def tools(self) -> tuple[Tool, ...]:
        return self._tools

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
        Executes one complete agent session.

        Concrete agents determine how reasoning and tool
        invocation are coordinated.
        """
        raise NotImplementedError
