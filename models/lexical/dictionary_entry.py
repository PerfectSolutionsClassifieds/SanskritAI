"""
SanskritAI
==========

Module:
    models.lexical.dictionary_entry

Description:
    Represents one dictionary record associated with a canonical Lexeme.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.enums.dictionary_source import DictionarySource

from .dictionary_sense import DictionarySense


@dataclass(slots=True)
class DictionaryEntry:
    """
    One dictionary's lexical record.

    Example
    -------
    राम

        ├── Amarakośa
        ├── Monier-Williams
        ├── Apte
        └── Vācaspatyam

    Each of the above is represented by one DictionaryEntry.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    entry_id: str

    source: DictionarySource

    headword: str

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------

    senses: list[DictionarySense] = field(default_factory=list)

    source_reference: str = ""

    notes: str = ""

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Validate and normalize the object.
        """

        self.entry_id = self.entry_id.strip()
        self.headword = self.headword.strip()
        self.source_reference = self.source_reference.strip()
        self.notes = self.notes.strip()

        if not self.entry_id:
            raise ValueError("entry_id cannot be empty.")

        if not self.headword:
            raise ValueError("headword cannot be empty.")

    # ---------------------------------------------------------
    # Computed Properties
    # ---------------------------------------------------------

    @property
    def identity(self) -> tuple[DictionarySource, str]:
        """
        Canonical identity.

        Uses (source, entry_id) because entry IDs are expected
        to be unique within a dictionary.
        """

        return (self.source, self.entry_id)

    @property
    def source_key(self) -> str:
        """
        Human-readable lookup key.

        Example
        -------
        AMARAKOSHA:राम
        """

        return f"{self.source.name}:{self.headword}"

    @property
    def sense_count(self) -> int:
        """
        Number of semantic senses.
        """

        return len(self.senses)

    # ---------------------------------------------------------
    # Operations
    # ---------------------------------------------------------

    def add_sense(
        self,
        sense: DictionarySense,
    ) -> None:
        """
        Add a semantic sense.

        Duplicate sense IDs are ignored.
        """

        if any(s.sense_id == sense.sense_id for s in self.senses):
            return

        self.senses.append(sense)

    def get_sense(
        self,
        sense_id: str,
    ) -> DictionarySense | None:
        """
        Retrieve a semantic sense by its ID.
        """

        for sense in self.senses:
            if sense.sense_id == sense_id:
                return sense

        return None

    def has_sense(
        self,
        sense_id: str,
    ) -> bool:
        """
        Determine whether a semantic sense exists.
        """

        return self.get_sense(sense_id) is not None

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize to a JSON-compatible dictionary.
        """

        return {
            "entry_id": self.entry_id,
            "source": self.source.value,
            "headword": self.headword,
            "source_reference": self.source_reference,
            "notes": self.notes,
            "sense_count": self.sense_count,
            "senses": [
                sense.to_dict()
                for sense in self.senses
            ],
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return f"{self.source.value}: {self.headword}"

    def __repr__(self) -> str:
        return (
            "DictionaryEntry("
            f"id='{self.entry_id}', "
            f"source='{self.source.name}', "
            f"headword='{self.headword}', "
            f"senses={self.sense_count})"
        )
