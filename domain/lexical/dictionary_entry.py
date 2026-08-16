
from __future__ import annotations

"""
SanskritAI
==========

Dictionary Entry
----------------

Domain model representing a lexical dictionary entry.

A DictionaryEntry provides the dictionary-level identity of a lexical
item and connects that identity to its lemma and dictionary source.

The model is deliberately small at this stage. Detailed meanings,
grammatical information, relations, and source metadata belong to
their respective domain objects and validators.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DictionaryEntry:
    """
    Immutable dictionary entry.

    Parameters
    ----------
    identifier:
        Stable identifier for the dictionary entry.

    lemma:
        Canonical lexical form represented by the entry.

    language:
        Language of the lexical entry.

    source:
        Dictionary or lexical source from which the entry originates.

    transliteration:
        Optional transliterated representation of the lemma.

    description:
        Optional short description of the entry.

    senses:
        Immutable collection of associated dictionary-sense identifiers.
        Detailed DictionarySense objects belong to the sense layer.
    """

    identifier: str
    lemma: str
    language: str = "Sanskrit"
    source: str = ""
    transliteration: str = ""
    description: str = ""
    senses: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """
        Normalize collection-like input while preserving immutability.
        """

        if not isinstance(self.senses, tuple):
            object.__setattr__(
                self,
                "senses",
                tuple(self.senses),
            )

    @property
    def has_senses(self) -> bool:
        """
        Return True when the entry contains at least one sense.
        """
        return bool(self.senses)

    @property
    def sense_count(self) -> int:
        """
        Return the number of associated sense identifiers.
        """
        return len(self.senses)

    @property
    def is_empty(self) -> bool:
        """
        Return True when the essential lexical content is absent.
        """
        return not self.identifier.strip() and not self.lemma.strip()
