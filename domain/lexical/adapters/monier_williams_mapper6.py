
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Mapper
----------------------

The Monier-Williams adapter has two explicit boundaries:

    Acquisition SourceRecord
            |
            v
    MonierWilliamsRecord
            |
            v
    CanonicalDictionaryEntry / Sense

The first boundary normalizes the acquisition representation.

The second boundary maps the normalized adapter record into the
canonical SanskritAI knowledge model.

The mapper performs domain construction only.

It does NOT:

* register lexicons
* mutate repositories
* perform repository lookup
* build indexes
* perform linguistic inference

Version
-------
v1.3.0
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

from SanskritAI.acquisition.lexical.monier_williams.monier_williams_source_record import (
    MonierWilliamsSourceRecord,
)

from .monier_williams_record import (
    MonierWilliamsRecord,
)


class MonierWilliamsMapper:
    """
    Maps Monier-Williams acquisition and adapter records into
    canonical knowledge objects.
    """

    SOURCE = "monier-williams"
    SOURCE_NAME = "Monier-Williams"
    SOURCE_VERSION = "unknown"

    # =========================================================
    # SourceRecord -> MonierWilliamsRecord
    # =========================================================

    @classmethod
    def from_source_record(
        cls,
        record: MonierWilliamsSourceRecord,
    ) -> MonierWilliamsRecord:
        """
        Normalize an acquisition-stage SourceRecord into the
        domain adapter record.

        This is the explicit boundary between:

            acquisition representation
                ->
            normalized lexical representation
        """

        if not isinstance(
            record,
            MonierWilliamsSourceRecord,
        ):
            raise TypeError(
                "record must be a MonierWilliamsSourceRecord"
            )

        fields = record.fields

        headword = (
            record.headword
            or fields.get("k1", "")
            or fields.get("headword", "")
        ).strip()

        definition = (
            record.definition
            or fields.get("e", "")
            or fields.get("definition", "")
        ).strip()

        if not headword:
            raise ValueError(
                "Monier-Williams SourceRecord has no headword"
            )

        if not definition:
            raise ValueError(
                "Monier-Williams SourceRecord has no definition"
            )

        transliteration = (
            record.transliteration
            or fields.get("transliteration", "")
        ).strip()

        grammatical_label = (
            record.grammatical_label
            or fields.get("grammatical_label", "")
            or fields.get("h", "")
        ).strip()

        grammatical_category = (
            record.grammatical_category
            or fields.get("grammatical_category", "")
        ).strip()

        source = (
            record.source
            or fields.get("source", "")
            or cls.SOURCE
        ).strip()

        source_id = (
            record.source_id
            or fields.get("source_id", "")
        ).strip()

        source_reference = (
            record.source_reference
            or fields.get("source_reference", "")
        ).strip()

        homonym = (
            record.homonym
            or fields.get("homonym", "")
            or fields.get("L", "")
        ).strip()

        return MonierWilliamsRecord(
            headword=headword,
            transliteration=transliteration,
            definition=definition,
            grammatical_label=grammatical_label,
            grammatical_category=grammatical_category,
            source=source or cls.SOURCE,
            source_id=source_id,
            source_reference=source_reference,
            raw_text=record.raw_text,
            homonym=homonym,
        )

    # =========================================================
    # Validation
    # =========================================================

    @staticmethod
    def _validate_record(
        record: MonierWilliamsRecord,
    ) -> None:
        if not isinstance(
            record,
            MonierWilliamsRecord,
        ):
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

        entry_id = (
            record.source_id
            or record.headword
        )

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
                "source_reference": (
                    record.source_reference
                ),
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

        cls._validate_record(record)

        resolved_entry_id = (
            cls._resolve_entry_id(record)
            if entry_id is None
            else entry_id
        )

        if not isinstance(
            resolved_entry_id,
            str,
        ):
            raise TypeError(
                "entry_id must be a string"
            )

        resolved_entry_id = (
            resolved_entry_id.strip()
        )

        if not resolved_entry_id:
            raise ValueError(
                "entry_id must not be empty"
            )

        if not isinstance(
            sense_number,
            int,
        ):
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

        if not isinstance(
            identifier,
            str,
        ):
            raise TypeError(
                "sense_id must be a string"
            )

        identifier = identifier.strip()

        if not identifier:
            raise ValueError(
                "sense_id must not be empty"
            )

        source = cls.to_source(record)

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
            citation=(
                record.source_reference
                or None
            ),
            metadata={
                "entry_id": resolved_entry_id,
                "sense_number": sense_number,
                "source_id": record.source_id,
                "source_reference": (
                    record.source_reference
                ),
                "grammatical_label": (
                    record.grammatical_label
                ),
                "grammatical_category": (
                    record.grammatical_category
                ),
                "homonym": record.homonym,
                "transliteration": (
                    record.transliteration
                ),
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
                record.transliteration
                or None
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
            citation=(
                record.source_reference
                or None
            ),
            metadata={
                "source_id": record.source_id,
                "source_reference": (
                    record.source_reference
                ),
                "grammatical_label": (
                    record.grammatical_label
                ),
                "grammatical_category": (
                    record.grammatical_category
                ),
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

        return tuple(
            cls.to_entry(record)
            for record in records
        )
