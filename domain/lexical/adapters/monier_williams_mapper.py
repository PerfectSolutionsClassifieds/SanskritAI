
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Mapper
----------------------

Converts a normalized Monier-Williams adapter record into the
canonical lexical models.

Architecture
------------

MonierWilliamsRecord
        |
        +-----------------------------+
        |                             |
        v                             v
DictionaryEntry                DictionarySense
        |                             |
        v                             v
DictionaryEntryMetadata       DictionarySenseMetadata
        |
        v
LexicalSource

Design Principles
-----------------

1. Source-specific acquisition remains outside the canonical model layer.
2. The mapper performs deterministic structural mapping only.
3. No linguistic inference is performed here.
4. Canonical lexical models are imported from ``lexical.models``.
5. The mapper does not persist anything.
"""

from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)
from SanskritAI.lexical.models.dictionary_entry_metadata import (
    DictionaryEntryMetadata,
)
from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)
from SanskritAI.lexical.models.dictionary_sense_metadata import (
    DictionarySenseMetadata,
)
from SanskritAI.lexical.models.lexical_source import (
    LexicalSource,
)

from .monier_williams_record import (
    MonierWilliamsRecord,
)


class MonierWilliamsMapper:
    """
    Maps normalized Monier-Williams records into canonical
    SanskritAI lexical models.
    """

    SOURCE = "monier-williams"
    SOURCE_NAME = "Monier-Williams"

    # =========================================================
    # Source
    # =========================================================

    @classmethod
    def to_source(
        cls,
        record: MonierWilliamsRecord,
    ) -> LexicalSource:
        """
        Convert the source information in an MW record into
        the canonical LexicalSource object.
        """

        if not isinstance(record, MonierWilliamsRecord):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

        identifier = (
            record.source.strip()
            if isinstance(record.source, str)
            and record.source.strip()
            else cls.SOURCE
        )

        return LexicalSource(
            identifier=identifier,
            name=cls.SOURCE_NAME,
        )

    # =========================================================
    # Entry
    # =========================================================

    @classmethod
    def to_entry(
        cls,
        record: MonierWilliamsRecord,
    ) -> DictionaryEntry:
        """
        Convert one normalized MW record into a canonical
        DictionaryEntry.
        """

        if not isinstance(record, MonierWilliamsRecord):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

        headword = record.headword.strip()

        if not headword:
            raise ValueError(
                "Monier-Williams record headword must not be empty."
            )

        identifier = (
            record.source_id.strip()
            if isinstance(record.source_id, str)
            and record.source_id.strip()
            else headword
        )

        metadata = DictionaryEntryMetadata(
            dictionary_name=cls.SOURCE_NAME,
            dictionary_version="",
            entry_identifier=identifier,
            headword=headword,
            lemma=headword,
            transliteration=(
                record.transliteration.strip()
                if isinstance(record.transliteration, str)
                else ""
            ),
            language="sa",
            page="",
            entry_number="",
            notes=(
                record.raw_text
                if isinstance(record.raw_text, str)
                else ""
            ),
            is_primary=True,
        )

        return DictionaryEntry(
            identifier=identifier,
            metadata=metadata,
            source=cls.to_source(record),
        )

    # =========================================================
    # Sense
    # =========================================================

    @classmethod
    def to_sense(
        cls,
        record: MonierWilliamsRecord,
        *,
        entry_id: str | None = None,
        sense_id: str | None = None,
        sense_number: int = 1,
    ) -> DictionarySense:
        """
        Convert one normalized MW record into a canonical
        DictionarySense.
        """

        if not isinstance(record, MonierWilliamsRecord):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

        resolved_entry_id = (
            entry_id.strip()
            if isinstance(entry_id, str)
            and entry_id.strip()
            else (
                record.source_id.strip()
                if isinstance(record.source_id, str)
                and record.source_id.strip()
                else record.headword.strip()
            )
        )

        if not resolved_entry_id:
            raise ValueError(
                "Unable to determine DictionarySense entry identifier."
            )

        identifier = (
            sense_id.strip()
            if isinstance(sense_id, str)
            and sense_id.strip()
            else f"{resolved_entry_id}:{sense_number}"
        )

        grammatical_note_parts: list[str] = []

        if (
            isinstance(record.grammatical_label, str)
            and record.grammatical_label.strip()
        ):
            grammatical_note_parts.append(
                record.grammatical_label.strip()
            )

        if (
            isinstance(record.grammatical_category, str)
            and record.grammatical_category.strip()
        ):
            grammatical_note_parts.append(
                record.grammatical_category.strip()
            )

        grammatical_note = "; ".join(
            grammatical_note_parts
        )

        metadata = DictionarySenseMetadata(
            sense_number=sense_number,
            definition=(
                record.definition.strip()
                if isinstance(record.definition, str)
                else ""
            ),
            short_definition=(
                record.definition.strip()
                if isinstance(record.definition, str)
                else ""
            ),
            gloss="",
            semantic_domain="",
            usage_label=(
                record.grammatical_label.strip()
                if isinstance(record.grammatical_label, str)
                else ""
            ),
            register="",
            grammatical_note=grammatical_note,
            etymology="",
            examples=[],
            citations=(
                [record.source_reference]
                if (
                    isinstance(record.source_reference, str)
                    and record.source_reference.strip()
                )
                else []
            ),
            cross_references=[],
            language="en",
            notes="",
        )

        return DictionarySense(
            identifier=identifier,
            metadata=metadata,
        )

    # =========================================================
    # Entry + Sense
    # =========================================================

    @classmethod
    def to_entry_and_sense(
        cls,
        record: MonierWilliamsRecord,
        *,
        sense_number: int = 1,
    ) -> tuple[DictionaryEntry, DictionarySense]:
        """
        Convert one MW record into its canonical entry and
        first canonical sense.
        """

        entry = cls.to_entry(record)

        sense = cls.to_sense(
            record,
            entry_id=entry.identifier,
            sense_number=sense_number,
        )

        return entry, sense
