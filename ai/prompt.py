from __future__ import annotations

"""
SanskritAI
==========

Prompt

Defines an immutable instantiated prompt derived from a
PromptTemplate.

A Prompt is the concrete prompt supplied to an AI model.

Architecture
------------

PromptTemplate
        │
        ▼
Prompt
        │
        ▼
AIRequest

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.ai.prompt_template import PromptTemplate
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Prompt(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable instantiated prompt.
    """

    template: PromptTemplate

    content: str

    values: frozenset[tuple[str, object]] = field(
        default_factory=frozenset,
    )

    @property
    def identifier(self) -> str:
        return self.template.identifier

    @property
    def display_name(self) -> str:
        return self.template.display_name

    @property
    def display_text(self) -> str:
        return self.template.display_text

    @property
    def display_description(self) -> str:
        return self.template.display_description

    @property
    def variables(self) -> frozenset[str]:
        return self.template.variables

    @property
    def variable_count(self) -> int:
        return self.template.variable_count

    @property
    def has_variables(self) -> bool:
        return self.template.has_variables

    def value(
        self,
        name: str,
        default=None,
    ):
        """
        Returns the bound value for a template variable.
        """
        return dict(self.values).get(name, default)

    def __str__(self) -> str:
        return self.display_text
