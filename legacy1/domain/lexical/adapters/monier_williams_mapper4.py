
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Mapper
----------------------

Maps normalized Monier-Williams adapter records into the
canonical SanskritAI knowledge model.

Pipeline
--------

MonierWilliamsRecord
        │
        ├──────────────► CanonicalSource
        │
        └──────────────► CanonicalDictionarySense
                              │
                              ▼
                       CanonicalDictionaryEntry

The mapper performs domain construction only.

It does NOT:
    • register lexicons
    • mutate repositories
    • perform repository lookup
    • build indexes
    • perform linguistic inference

Compatibility
-------------

The mapper preserves the established public mapper operations:

    to_source()
    to_entry()
    to_sense()
    to_entry_and_sense()

The returned objects are now canonical objects.

Version
-------
v1.1.0
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
    Maps normalized Monier-Williams records into canonical
    knowledge objects.
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

        The source object represents the dictionary resource,
        not the individual dictionary record.
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
        entry_id: str,
        sense_id: str | None = None,
        sense_number: int = 1,
    ) -> CanonicalDictionarySense:
        """
        Convert one MW record into a canonical dictionary sense.

        Parameters
        ----------
        record:
            Normalized MW record.

        entry_id:
            Stable lexical entry identifier used as the basis
            for the sense identifier.

        sense_id:
            Optional explicit sense identifier.

        sense_number:
            Explicit sense number used when no sense_id is
            supplied.

        Examples
        --------
        entry_id="MW-hari"
        sense_number=3

        produces:

            MW-hari:3
        """

        cls._validate_record(record)

        if not isinstance(entry_id, str):
            raise TypeError(
                "entry_id must be a string"
            )

        if not entry_id.strip():
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
            or f"{entry_id}:{sense_number}"
        )

        source = cls.to_source(record)

        part_of_speech = (
            record.grammatical_category
            or record.grammatical_label
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
                "entry_id": entry_id,
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

        entry_id = (
            record.source_id
            or record.headword
        )

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
                record.grammatical_category
                or None
            ),
            senses=(sense,),
            source_name=(
                record.source
                or cls.SOURCE_NAME
            ),
            source_version=cls.SOURCE_VERSION,
            source_record_id=entry_id,
            citation=record.source_reference or None,
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

        The resulting entry owns its canonical sense.
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
