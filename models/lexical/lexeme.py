"""
SanskritAI
==========

Module:
    models.lexical.lexeme

Description:
    Canonical lexical entity.

    Every Sanskrit word occurring anywhere in the system ultimately
    resolves to one Lexeme object.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.enums.dictionary_source import DictionarySource
from models.enums.language import Language
from models.enums.script import Script

from .dictionary_entry import DictionaryEntry
from .lexical_relation import LexicalRelation


@dataclass(slots=True)
class Lexeme:
    """
    Canonical lexical object.

    Examples
    --------
        रामः
        रामम्
        रामेण
        रामस्य

    all resolve to

        राम
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    lexeme_id: str

    lemma: str

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    language: Language = Language.SANSKRIT

    script: Script = Script.DEVANAGARI

    transliteration: str = ""

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    etymology: str = ""

    notes: str = ""

    # ---------------------------------------------------------
    # Collections
    # ---------------------------------------------------------

    dictionary_entries: list[DictionaryEntry] = field(default_factory=list)

    relations: list[LexicalRelation] = field(default_factory=list)

    # ---------------------------------------------------------
    # Internal Indexes
    # ---------------------------------------------------------

    _dictionary_index: dict[
        DictionarySource,
        DictionaryEntry
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Validate the object and rebuild lookup indexes.

        The index is reconstructed automatically after
        JSON deserialization.
        """

        self.lexeme_id = self.lexeme_id.strip()
        self.lemma = self.lemma.strip()

        if not self.lexeme_id:
            raise ValueError("lexeme_id cannot be empty.")

        if not self.lemma:
            raise ValueError("lemma cannot be empty.")

        for entry in self.dictionary_entries:
            self._dictionary_index[entry.source] = entry

    # ---------------------------------------------------------
    # Dictionary Operations
    # ---------------------------------------------------------

    def add_dictionary_entry(
        self,
        entry: DictionaryEntry,
    ) -> None:
        """
        Add or replace a dictionary entry.

        Only one entry per DictionarySource is maintained.
        """

        existing = self._dictionary_index.get(entry.source)

        if existing is not None:
            index = self.dictionary_entries.index(existing)
            self.dictionary_entries[index] = entry
        else:
            self.dictionary_entries.append(entry)

        self._dictionary_index[entry.source] = entry

    def get_entry(
        self,
        source: DictionarySource,
    ) -> DictionaryEntry | None:
        """
        Retrieve a dictionary entry in O(1) time.
        """

        return self._dictionary_index.get(source)

    def has_entry(
        self,
        source: DictionarySource,
    ) -> bool:
        """
        Determine whether a dictionary entry exists.
        """

        return source in self._dictionary_index

    def remove_entry(
        self,
        source: DictionarySource,
    ) -> bool:
        """
        Remove one dictionary entry.

        Returns
        -------
        bool
            True if removed.
        """

        entry = self._dictionary_index.pop(source, None)

        if entry is None:
            return False

        self.dictionary_entries.remove(entry)

        return True

    # ---------------------------------------------------------
    # Relation Operations
    # ---------------------------------------------------------

    def add_relation(
        self,
        relation: LexicalRelation,
    ) -> None:
        """
        Add a lexical relation.

        Duplicate relation IDs are ignored.
        """

        if any(
            r.relation_id == relation.relation_id
            for r in self.relations
        ):
            return

        self.relations.append(relation)

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def dictionary_count(self) -> int:
        """
        Number of dictionary entries.
        """

        return len(self.dictionary_entries)

    @property
    def relation_count(self) -> int:
        """
        Number of lexical relations.
        """

        return len(self.relations)

    @property
    def dictionary_sources(self) -> tuple[DictionarySource, ...]:
        """
        Immutable collection of available dictionary sources.

        Returned in deterministic order for reproducible
        serialization and testing.
        """

        return tuple(
            sorted(
                self._dictionary_index.keys(),
                key=lambda source: source.value,
            )
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Serialize to a JSON-compatible dictionary.
        """

        return {
            "lexeme_id": self.lexeme_id,
            "lemma": self.lemma,
            "language": self.language.value,
            "script": self.script.value,
            "transliteration": self.transliteration,
            "etymology": self.etymology,
            "notes": self.notes,
            "dictionary_entries": [
                entry.to_dict()
                for entry in self.dictionary_entries
            ],
            "relations": [
                relation.to_dict()
                for relation in self.relations
            ],
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.lemma

    def __repr__(self) -> str:
        return (
            "Lexeme("
            f"id='{self.lexeme_id}', "
            f"lemma='{self.lemma}', "
            f"dictionaries={self.dictionary_count}, "
            f"relations={self.relation_count})"
        )
