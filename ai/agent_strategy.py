from __future__ import annotations

"""
SanskritAI
==========

Agent Strategy

Defines the abstract policy governing how an Agent performs
its work.

An AgentStrategy encapsulates the execution algorithm,
while the Agent coordinates the overall lifecycle.

Architecture
------------

KnowledgeContext
        │
        ▼
AgentStrategy
        │
        ▼
Agent

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.ai.knowledge_context import KnowledgeContext
from SanskritAI.core.mixins.displayable import Displayable


class AgentStrategy(
    ABC,
    Displayable,
):
    """
    Abstract Agent strategy.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Agent strategy."

    @abstractmethod
    def execute(
        self,
        context: KnowledgeContext,
    ) -> object:
        """
        Executes one agent session according to this strategy.
        """
        raise NotImplementedError
