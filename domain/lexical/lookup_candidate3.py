
from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


@dataclass(frozen=True, slots=True)
class LookupCandidate:
    """
    Candidate returned by lexical lookup.

    The candidate wraps a canonical dictionary entry together with an
    optional sense, matching information, and ranking score.

    During the transition to the canonical knowledge model, identifier
    resolution supports both:

        CanonicalDictionaryEntry.source_record_id
        legacy entry.entry_id

    Canonical entries should use ``source_record_id``.
    """

    entry: CanonicalDictionaryEntry
    sense: CanonicalDictionarySense | None = None
    score: float = 1.0
    matched_word_form: str = ""
    normalized_word_form: str = ""

    @property
    def identifier(self) -> str:
        """
        Return the source-level entry identity.

        CanonicalDictionaryEntry uses ``source_record_id`` as its
        source-level identity.

        A temporary ``entry_id`` fallback is retained for compatibility
        with existing domain tests and legacy entry-like objects.
        """
        source_record_id = getattr(
            self.entry,
            "source_record_id",
            None,
        )

        if source_record_id:
            return str(source_record_id)

        legacy_entry_id = getattr(
            self.entry,
            "entry_id",
            None,
        )

        if legacy_entry_id:
            return str(legacy_entry_id)

        return str(
            getattr(
                self.entry,
                "headword",
                "",
            )
        )

    @property
    def headword(self) -> str:
        """
        Return the candidate entry headword.
        """
        return str(
            getattr(
                self.entry,
                "headword",
                "",
            )
        )

    @property
    def has_sense(self) -> bool:
        """
        Return True when a dictionary sense is attached.
        """
        return self.sense is not None

    @property
    def confidence(self) -> float:
        """
        Return the candidate confidence/ranking score.
        """
        return self.score

    def __str__(self) -> str:
        """
        Human-readable candidate representation.
        """
        if self.sense is not None:
            return (
                f"{self.headword} "
                f"(score={self.score:.3f})"
            )

        return (
            f"{self.headword} "
            f"(score={self.score:.3f})"
        )
