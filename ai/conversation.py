from __future__ import annotations

"""
SanskritAI
==========

Conversation

Defines an immutable conversation composed of one or more
Prompt objects.

A Conversation represents the declarative conversational
context supplied to reasoning engines and AI agents.

The Conversation itself owns no execution behavior.

Architecture
------------

Prompt
    │
    ▼
Conversation
    │
    ▼
Reasoner

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.ai.prompt import Prompt
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Conversation(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable conversation.

    A conversation is an ordered sequence of prompts.
    """

    identifier: str

    name: str

    prompts: tuple[Prompt, ...] = field(
        default_factory=tuple,
    )

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def is_empty(self) -> bool:
        return len(self.prompts) == 0

    @property
    def prompt_count(self) -> int:
        return len(self.prompts)

    def add_prompt(
        self,
        prompt: Prompt,
    ) -> "Conversation":
        """
        Returns a new Conversation with the supplied Prompt
        appended.
        """
        return Conversation(
            identifier=self.identifier,
            name=self.name,
            prompts=self.prompts + (prompt,),
            description=self.description,
        )

    def __iter__(self) -> Iterator[Prompt]:
        return iter(self.prompts)

    def __len__(self) -> int:
        return len(self.prompts)

    def __str__(self) -> str:
        return self.display_text
