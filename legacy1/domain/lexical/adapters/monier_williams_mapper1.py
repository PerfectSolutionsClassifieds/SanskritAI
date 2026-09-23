from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Mapper
----------------------

Converts normalized Monier-Williams adapter records into the
canonical lexical-domain models.

The mapper is intentionally separate from the adapter so that:

    acquisition
        !=
    normalization
        !=
    domain construction
"""

from SanskritAI.domain.lexical.dictionary_entry import (
    DictionaryEntry,
)
from SanskritAI.domain.lexical.dictionary_sense import (
    DictionarySense,
)

from .monier_williams_record import (
    MonierWilliamsRecord,
)


class MonierWilliamsMapper:
    """
    Maps normalized Monier-Williams records to domain objects.
    """

    SOURCE = "monier-williams"

    @classmethod
    def to_entry(
        cls,
        record: MonierWilliamsRecord,
    ) -> DictionaryEntry:
        """
        Convert one MW record into a DictionaryEntry.
        """

        if not isinstance(record, MonierWilliamsRecord):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

        identifier = (
            record.source_id
            or record.headword
        )

        return DictionaryEntry(
            identifier=identifier,
            lemma=record.headword,
            language="sa",
            source=record.source,
            transliteration=record.transliteration,
            description=record.definition,
            senses=(),
        )

    @classmethod
    def to_sense(
        cls,
        record: MonierWilliamsRecord,
        *,
        entry_id: str,
        sense_id: str | None = None,
    ) -> DictionarySense:
        """
        Convert one MW record into a DictionarySense.
        """

        if not isinstance(record, MonierWilliamsRecord):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

        identifier = (
            sense_id
            or f"{entry_id}:1"
        )

        return DictionarySense(
            identifier=identifier,
            entry_id=entry_id,
            meaning=record.definition,
            language="en",
            source=record.source,
            transliteration=record.transliteration,
            grammatical_label=record.grammatical_label,
            usage="",
            examples=(),
        )
