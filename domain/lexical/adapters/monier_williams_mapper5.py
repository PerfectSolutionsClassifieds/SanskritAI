
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Mapper
----------------------

Maps normalized Monier-Williams adapter records into the canonical
SanskritAI knowledge model.

Pipeline
--------

    MonierWilliamsRecord
            |
            +-------------> CanonicalSource
            |
            +-------------> CanonicalDictionarySense
                                      |
                                      v
                              CanonicalDictionaryEntry

The mapper performs domain construction only.

It does NOT:

* register lexicons
* mutate repositories
* perform repository lookup
* build indexes
* perform linguistic inference

Canonical public operations
---------------------------

    to_source()
    to_entry()
    to_sense()
    to_entry_and_sense()
    to_entries()

Version
-------

v1.2.0
"""

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)
from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)

from .monier_williams_record import (
    MonierWilliamsRecord,
)


class MonierWilliamsMapper:
    """
    Maps normalized Monier-Williams records into canonical knowledge objects.
    """

    SOURCE = "monier-williams"
    SOURCE_NAME = "Monier-Williams"
    SOURCE_VERSION = "unknown"

    # =========================================================
    # Validation
    # =========================================================

    @staticmethod
    def _validate_record(
        record: MonierWilliamsRecord,
    ) -> None:
        if not isinstance(record, MonierWilliamsRecord):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

    @staticmethod
    def _resolve_entry_id(
        record: MonierWilliamsRecord,
    ) -> str:
        """
        Resolve the stable entry identifier.

        Preference:

        1. source_id
        2. headword
        """
        entry_id = record.source_id or record.headword

        if not isinstance(entry_id, str):
            raise TypeError(
                "resolved entry_id must be a string"
            )

        entry_id = entry_id.strip()

        if not entry_id:
            raise ValueError(
                "resolved entry_id must not be empty"
            )

        return entry_id

    # =========================================================
    # Canonical Source
    # =========================================================

    @classmethod
    def to_source(
        cls,
        record: MonierWilliamsRecord,
    ) -> CanonicalSource:
        """
        Convert an MW record into the canonical source object.

        The source represents the Monier-Williams dictionary resource,
        not the individual lexical entry.
        """
        cls._validate_record(record)

        return CanonicalSource(
            source_id=cls.SOURCE,
            name=cls.SOURCE_NAME,
            short_name="MW",
            source_type="lexicon",
            language="sa",
            script="Devanagari",
            author="Monier Monier-Williams",
            publisher="Clarendon Press, Oxford",
            edition=None,
            publication_year=1899,
            version=cls.SOURCE_VERSION,
            metadata={
                "record_id": record.source_id,
                "source_reference": record.source_reference,
                "homonym": record.homonym,
            },
        )

    # =========================================================
    # Canonical Sense
    # =========================================================

    @classmethod
    def to_sense(
        cls,
        record: MonierWilliamsRecord,
        *,
        entry_id: str | None = None,
        sense_id: str | None = None,
        sense_number: int = 1,
    ) -> CanonicalDictionarySense:
        """
        Convert one MW record into a canonical dictionary sense.

        ``entry_id`` is optional.

        If omitted, it is resolved from:

            record.source_id
            record.headword

        ``sense_number`` is retained in canonical metadata because
        CanonicalDictionarySense does not expose a dedicated
        ``sense_number`` field.
        """
        cls._validate_record(record)

        resolved_entry_id = (
            cls._resolve_entry_id(record)
            if entry_id is None
            else entry_id
        )

        if not isinstance(resolved_entry_id, str):
            raise TypeError(
                "entry_id must be a string"
            )

        resolved_entry_id = resolved_entry_id.strip()

        if not resolved_entry_id:
            raise ValueError(
                "entry_id must not be empty"
            )

        if not isinstance(sense_number, int):
            raise TypeError(
                "sense_number must be an integer"
            )

        if sense_number <= 0:
            raise ValueError(
                "sense_number must be positive"
            )

        identifier = (
            sense_id
            or f"{resolved_entry_id}:{sense_number}"
        )

        if not isinstance(identifier, str):
            raise TypeError(
                "sense_id must be a string"
            )

        identifier = identifier.strip()

        if not identifier:
            raise ValueError(
                "sense_id must not be empty"
            )

        source = cls.to_source(record)

        # The traditional MW grammatical label, such as "m.",
        # is the most direct grammatical classification for the
        # canonical sense. The broader category remains in metadata.
        part_of_speech = (
            record.grammatical_label
            or record.grammatical_category
            or None
        )

        return CanonicalDictionarySense(
            sense_id=identifier,
            entry_headword=record.headword,
            definition=record.definition,
            source=source,
            part_of_speech=part_of_speech,
            citation=record.source_reference or None,
            metadata={
                "entry_id": resolved_entry_id,
                "sense_number": sense_number,
                "source_id": record.source_id,
                "source_reference": record.source_reference,
                "grammatical_label": record.grammatical_label,
                "grammatical_category": record.grammatical_category,
                "homonym": record.homonym,
                "transliteration": record.transliteration,
                "raw_text": record.raw_text,
            },
        )

    # =========================================================
    # Canonical Entry + Sense
    # =========================================================

    @classmethod
    def to_entry_and_sense(
        cls,
        record: MonierWilliamsRecord,
        *,
        sense_id: str | None = None,
        sense_number: int = 1,
    ) -> tuple[
        CanonicalDictionaryEntry,
        CanonicalDictionarySense,
    ]:
        """
        Convert one MW record into a matching canonical
        entry/sense pair.

        The returned entry owns the returned sense.
        """
        cls._validate_record(record)

        entry_id = cls._resolve_entry_id(record)

        sense = cls.to_sense(
            record,
            entry_id=entry_id,
            sense_id=sense_id,
            sense_number=sense_number,
        )

        entry = CanonicalDictionaryEntry(
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
                record.source
                or cls.SOURCE_NAME
            ),
            source_version=cls.SOURCE_VERSION,
            source_record_id=entry_id,
            citation=(
                record.source_reference or None
            ),
            metadata={
                "source_id": record.source_id,
                "source_reference": record.source_reference,
                "grammatical_label": record.grammatical_label,
                "grammatical_category": record.grammatical_category,
                "homonym": record.homonym,
                "raw_text": record.raw_text,
            },
        )

        return entry, sense

    # =========================================================
    # Canonical Entry
    # =========================================================

    @classmethod
    def to_entry(
        cls,
        record: MonierWilliamsRecord,
        *,
        sense_id: str | None = None,
        sense_number: int = 1,
    ) -> CanonicalDictionaryEntry:
        """
        Convert one MW record into a canonical dictionary entry.
        """
        entry, _ = cls.to_entry_and_sense(
            record,
            sense_id=sense_id,
            sense_number=sense_number,
        )

        return entry

    # =========================================================
    # Batch
    # =========================================================

    @classmethod
    def to_entries(
        cls,
        records: (
            tuple[MonierWilliamsRecord, ...]
            | list[MonierWilliamsRecord]
        ),
    ) -> tuple[CanonicalDictionaryEntry, ...]:
        """
        Convert multiple MW records into canonical entries.
        """
        return tuple(
            cls.to_entry(record)
            for record in records
        )
