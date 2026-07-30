from __future__ import annotations

"""
SanskritAI
==========

Token

Represents a concrete occurrence of a WordForm within a text.

Examples
--------

रामः appears in Bhagavad Gītā 2.1

विद्यया appears in Hitopadeśa

Relationship
------------

Lexeme
    │
Lemma
    │
WordForm
    │
Token

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.lexical.word_form import WordForm


@dataclass(frozen=True, slots=True)
class Token(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable textual token.
    """

    identifier: str

    word_form: WordForm

    text: str

    position: int = 0

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.text

    @property
    def display_text(self) -> str:
        return self.text

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def lemma(self):
        return self.word_form.lemma

    @property
    def canonical_form(self) -> str:
        return self.word_form.canonical_form

    @property
    def is_lemma(self) -> bool:
        return self.word_form.is_lemma

    def __str__(self) -> str:
        return self.text
