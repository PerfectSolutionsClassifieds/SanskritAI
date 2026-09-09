
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Mapper
----------------------

Converts a normalized Monier-Williams record directly into
the canonical lexical knowledge graph.

Pipeline
--------

MonierWilliamsRecord
        ↓
CanonicalDictionarySense
        ↓
CanonicalDictionaryEntry

The mapper performs domain construction only.

It does not:
    • register lexicons
    • mutate repositories
    • build indexes
    • perform lookup
    • perform linguistic inference

Version
-------
v1.0.0
"""

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from .monier_williams_record import (
    MonierWilliamsRecord,
)


class MonierWilliamsMapper:
    """
    Maps normalized Monier-Williams records into canonical
    dictionary entries and senses.
    """

    SOURCE_NAME = "Monier-Williams"

    # =========================================================
    # Sense
    # =========================================================

    @classmethod
    def to_sense(
        cls,
        record: MonierWilliamsRecord,
        *,
        entry_headword: str | None = None,
        sense_id: str | None = None,
    ) -> CanonicalDictionarySense:
        """
        Convert one normalized MW record into a canonical sense.
        """

        if not isinstance(record, MonierWilliamsRecord):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

        headword = entry_headword or record.headword

        identifier = (
            sense_id
            or f"{record.source_id or headword}:1"
        )

        return CanonicalDictionarySense(
            sense_id=identifier,
            entry_headword=headword,
            definition=record.definition,
            part_of_speech=record.grammatical_label or None,
            metadata={
                "source": record.source,
                "source_id": record.source_id,
                "source_reference": record.source_reference,
                "grammatical_category": record.grammatical_category,
                "homonym": record.homonym,
                "raw_text": record.raw_text,
                "transliteration": record.transliteration,
            },
        )

    # =========================================================
    # Entry
    # =========================================================

    @classmethod
    def to_entry(
        cls,
        record: MonierWilliamsRecord,
        *,
        sense_id: str | None = None,
    ) -> CanonicalDictionaryEntry:
        """
        Convert one normalized MW record into a canonical entry.

        The entry owns its canonical sense.
        """

        if not isinstance(record, MonierWilliamsRecord):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

        sense = cls.to_sense(
            record,
            entry_headword=record.headword,
            sense_id=sense_id,
        )

        return CanonicalDictionaryEntry(
            headword=record.headword,
            transliteration=(
                record.transliteration or None
            ),
            language="sa",
            script="Devanagari",
            lemma=record.headword,
            normalized_headword=record.headword,
            entry_type=(
                record.grammatical_category or None
            ),
            senses=(sense,),
            source_name=(
                record.source or cls.SOURCE_NAME
            ),
            source_version="",
            source_record_id=(
                record.source_id or record.headword
            ),
            metadata={
                "source_reference": record.source_reference,
                "grammatical_label": record.grammatical_label,
                "grammatical_category": record.grammatical_category,
                "homonym": record.homonym,
                "raw_text": record.raw_text,
            },
        )

    # =========================================================
    # Batch
    # =========================================================

    @classmethod
    def to_entries(
        cls,
        records: tuple[MonierWilliamsRecord, ...]
        | list[MonierWilliamsRecord],
    ) -> tuple[CanonicalDictionaryEntry, ...]:
        """
        Convert multiple MW records into canonical entries.
        """

        return tuple(
            cls.to_entry(record)
            for record in records
        )
