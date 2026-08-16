
from __future__ import annotations

"""
SanskritAI
==========

Dictionary Sense
----------------

Represents one dictionary-level semantic sense associated with
a DictionaryEntry.

The DictionarySense model deliberately represents the semantic
unit only. Detailed lexical relations, grammatical analysis,
examples, and external source mappings belong to their respective
domain layers.
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class DictionarySense(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable dictionary sense.

    Parameters
    ----------
    identifier:
        Stable identifier for the sense.

    entry_id:
        Identifier of the DictionaryEntry to which this sense
        belongs.

    meaning:
        Primary semantic meaning represented by this sense.

    language:
        Language of the meaning.

    source:
        Optional dictionary or lexical source.

    transliteration:
        Optional transliterated representation of the lexical form.

    grammatical_label:
        Optional grammatical or lexical-category label.

    usage:
        Optional usage information.

    examples:
        Optional immutable collection of example strings.
    """

    identifier: str
    entry_id: str
    meaning: str
    language: str = "sanskrit"
    source: str = ""
    transliteration: str = ""
    grammatical_label: str = ""
    usage: str = ""
    examples: tuple[str, ...] = ()

    @property
    def display_name(self) -> str:
        """
        Return the primary display name of the sense.
        """
        return self.meaning

    @property
    def display_text(self) -> str:
        """
        Return a concise human-readable representation.
        """
        if self.transliteration:
            return f"{self.meaning} ({self.transliteration})"

        return self.meaning

    @property
    def display_description(self) -> str:
        """
        Return descriptive usage information.
        """
        return self.usage

    @property
    def example_count(self) -> int:
        """
        Return the number of examples associated with the sense.
        """
        return len(self.examples)

    @property
    def has_examples(self) -> bool:
        """
        Return True when at least one example is present.
        """
        return bool(self.examples)

    @property
    def has_source(self) -> bool:
        """
        Return True when source information is present.
        """
        return bool(self.source)

    @property
    def has_grammatical_label(self) -> bool:
        """
        Return True when a grammatical label is present.
        """
        return bool(self.grammatical_label)

    @property
    def has_transliteration(self) -> bool:
        """
        Return True when transliteration is present.
        """
        return bool(self.transliteration)

    def __str__(self) -> str:
        """
        Return the display representation.
        """
        return self.display_text
