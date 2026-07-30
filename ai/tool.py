from __future__ import annotations

"""
SanskritAI
==========

Tool

Defines the abstract capability that an AI Agent may invoke.

A Tool encapsulates one executable capability while remaining
independent of any particular Agent implementation.

Architecture
------------

KnowledgeContext
        │
        ▼
Tool
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


class Tool(
    ABC,
    Displayable,
):
    """
    Abstract AI Tool.
    """

    @property
    def identifier(self) -> str:
        return self.__class__.__name__

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract AI tool."

    @abstractmethod
    def execute(
        self,
        context: KnowledgeContext,
    ) -> object:
        """
        Executes this tool using the supplied knowledge
        context.
        """
        raise NotImplementedError
