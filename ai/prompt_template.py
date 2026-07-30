from __future__ import annotations

"""
SanskritAI
==========

Prompt Template

Defines an immutable reusable prompt template.

A PromptTemplate represents the declarative structure from
which one or more Prompt instances may be created.

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

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PromptTemplate(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable prompt template.
    """

    identifier: str

    name: str

    template: str

    description: str = ""

    variables: frozenset[str] = field(
        default_factory=frozenset,
    )

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
    def variable_count(self) -> int:
        return len(self.variables)

    @property
    def has_variables(self) -> bool:
        return bool(self.variables)

    def supports(
        self,
        variable: str,
    ) -> bool:
        """
        Determines whether the template declares the supplied
        variable.
        """
        return variable in self.variables

    def __str__(self) -> str:
        return self.display_text
