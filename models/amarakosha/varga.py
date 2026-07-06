"""
SanskritAI
==========

Module:
    models.amarakosha.varga

Description
-----------
Represents one Varga (semantic chapter) of the Amarakośa.

A Varga contains an ordered collection of verses.

Examples
--------
    Svargavarga
    Bhūmivarga
    Puruṣavarga
    Vanauṣadhivarga

This class contains only domain information.

No parsing, importing, searching, or repository logic belongs here.

Version:
    v0.4.0
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .verse import Verse


@dataclass(slots=True)
class Varga:
    """
    Represents one Amarakośa Varga.

    Structure
    ---------

    Kāṇḍa

        └── Varga

              ├── Verse

              ├── Verse

              └── Verse
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    varga_id: str

    varga_number: int

    title: str

    # ---------------------------------------------------------
    # Optional Metadata
    # ---------------------------------------------------------

    english_title: str = ""

    theme: str = ""

    notes: str = ""

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------

    verses: list[Verse] = field(default_factory=list)

    # ---------------------------------------------------------
    # Internal Index
    # ---------------------------------------------------------

    _verse_index: dict[str, Verse] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def __post_init__(self) -> None:

        self.varga_id = self.varga_id.strip()

        self.title = self.title.strip()

        if not self.varga_id:
            raise ValueError(
                "varga_id cannot be empty."
            )

        if self.varga_number <= 0:
            raise ValueError(
                "varga_number must be positive."
            )

        if not self.title:
            raise ValueError(
                "title cannot be empty."
            )

        for verse in self.verses:
            self._verse_index[verse.verse_id] = verse

    # ---------------------------------------------------------
    # Verse Operations
    # ---------------------------------------------------------

    def add_verse(
        self,
        verse: Verse,
    ) -> None:
        """
        Add or replace a verse.
        """

        existing = self._verse_index.get(
            verse.verse_id
        )

        if existing is not None:

            index = self.verses.index(existing)

            self.verses[index] = verse

        else:

            self.verses.append(verse)

        self._verse_index[
            verse.verse_id
        ] = verse

    def get_verse(
        self,
        verse_id: str,
    ) -> Verse | None:

        return self._verse_index.get(verse_id)

    def remove_verse(
        self,
        verse_id: str,
    ) -> bool:

        verse = self._verse_index.pop(
            verse_id,
            None,
        )

        if verse is None:
            return False

        self.verses.remove(verse)

        return True

    def clear(self) -> None:

        self.verses.clear()

        self._verse_index.clear()

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    @property
    def verse_count(self) -> int:

        return len(self.verses)

    @property
    def first_verse(self) -> Verse | None:

        if not self.verses:
            return None

        return self.verses[0]

    @property
    def last_verse(self) -> Verse | None:

        if not self.verses:
            return None

        return self.verses[-1]

    @property
    def verse_ids(self) -> tuple[str, ...]:
        """
        Immutable list of Verse IDs.
        """

        return tuple(
            sorted(self._verse_index.keys())
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "varga_id": self.varga_id,

            "varga_number": self.varga_number,

            "title": self.title,

            "english_title": self.english_title,

            "theme": self.theme,

            "notes": self.notes,

            "verse_count": self.verse_count,

            "verses": [

                verse.to_dict()

                for verse in self.verses

            ],
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __len__(self) -> int:

        return self.verse_count

    def __iter__(self):

        return iter(self.verses)

    def __contains__(
        self,
        verse_id: str,
    ) -> bool:

        return verse_id in self._verse_index

    def __str__(self) -> str:

        return self.title

    def __repr__(self) -> str:

        return (
            "Varga("
            f"id='{self.varga_id}', "
            f"number={self.varga_number}, "
            f"title='{self.title}', "
            f"verses={self.verse_count})"
        )
