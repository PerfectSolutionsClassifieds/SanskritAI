
from __future__ import annotations

"""
SanskritAI
==========

Word Form
---------

Represents one grammatical realization of a Lemma.

Examples
--------
रामः
रामम्
रामेण
रामाय
विद्यया

Relationship
------------
Lemma
 │
 └── WordForm
       │
       └── Token

Version
-------
v1.0.1
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.lexical.lemma import Lemma


@dataclass(
    frozen=True,
    slots=True,
)
class WordForm(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable grammatical realization of a Lemma.

    Parameters
    ----------
    identifier:
        Stable identifier for the word form.

    lemma:
        Lemma from which this word form is derived.

    text:
        Surface Sanskrit form.

    transliteration:
        Optional transliterated representation.

    description:
        Optional human-readable description.
    """

    identifier: str
    lemma: Lemma
    text: str
    transliteration: str = ""
    description: str = ""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.text

    @property
    def display_text(self) -> str:
        if self.transliteration:
            return f"{self.text} ({self.transliteration})"

        return self.text

    @property
    def display_description(self) -> str:
        return self.description

    # ---------------------------------------------------------
    # Lexical Semantics
    # ---------------------------------------------------------

    @property
    def canonical_form(self) -> str:
        """
        Return the canonical citation form of the word.

        The canonical form is the lemma's textual representation.
        """
        return self.lemma.text

    @property
    def is_lemma(self) -> bool:
        """
        Return True when this word form is identical to its lemma.
        """
        return self.text == self.lemma.text

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
