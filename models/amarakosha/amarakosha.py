"""
SanskritAI
==========

Module:
    models.amarakosha.amarakosha

Description
-----------
Root domain model representing the complete Amarakośa.

Hierarchy
---------

    Amarakosha
        └── Kanda
              └── Varga
                    └── Verse

This class is intentionally independent of:

    • parsers
    • repositories
    • databases
    • importers
    • search engines

It represents only the canonical structure of the text.

Version:
    v0.4.0
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .kanda import Kanda


@dataclass(slots=True)
class Amarakosha:
    """
    Root object representing one complete Amarakośa edition.

    The object owns all Kāṇḍas and provides fast lookup,
    aggregate statistics, and serialization.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    edition_id: str

    title: str = "Amarakośa"

    # ---------------------------------------------------------
    # Bibliographic Metadata
    # ---------------------------------------------------------

    author: str = "Amarasiṃha"

    language: str = "Sanskrit"

    script: str = "Devanagari"

    version: str = "v0.4.0"

    source: str = ""

    editor: str = ""

    publisher: str = ""

    publication_year: str = ""

    notes: str = ""

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------

    kandas: list[Kanda] = field(default_factory=list)

    # ---------------------------------------------------------
    # Internal Index
    # ---------------------------------------------------------

    _kanda_index: dict[str, Kanda] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def __post_init__(self) -> None:

        self.edition_id = self.edition_id.strip()

        self.title = self.title.strip()

        if not self.edition_id:
            raise ValueError(
                "edition_id cannot be empty."
            )

        if not self.title:
            raise ValueError(
                "title cannot be empty."
            )

        for kanda in self.kandas:
            self._kanda_index[kanda.kanda_id] = kanda

    # ---------------------------------------------------------
    # Kāṇḍa Operations
    # ---------------------------------------------------------

    def add_kanda(
        self,
        kanda: Kanda,
    ) -> None:
        """
        Add or replace a Kāṇḍa.
        """

        existing = self._kanda_index.get(
            kanda.kanda_id
        )

        if existing is not None:

            index = self.kandas.index(existing)

            self.kandas[index] = kanda

        else:

            self.kandas.append(kanda)

        self._kanda_index[
            kanda.kanda_id
        ] = kanda

    def get_kanda(
        self,
        kanda_id: str,
    ) -> Kanda | None:

        return self._kanda_index.get(kanda_id)

    def remove_kanda(
        self,
        kanda_id: str,
    ) -> bool:

        kanda = self._kanda_index.pop(
            kanda_id,
            None,
        )

        if kanda is None:
            return False

        self.kandas.remove(kanda)

        return True

    def clear(self) -> None:

        self.kandas.clear()

        self._kanda_index.clear()

    # ---------------------------------------------------------
    # Aggregate Statistics
    # ---------------------------------------------------------

    @property
    def kanda_count(self) -> int:

        return len(self.kandas)

    @property
    def varga_count(self) -> int:

        return sum(
            kanda.varga_count
            for kanda in self.kandas
        )

    @property
    def verse_count(self) -> int:

        return sum(
            kanda.verse_count
            for kanda in self.kandas
        )

    @property
    def first_kanda(self) -> Kanda | None:

        if not self.kandas:
            return None

        return self.kandas[0]

    @property
    def last_kanda(self) -> Kanda | None:

        if not self.kandas:
            return None

        return self.kandas[-1]

    @property
    def kanda_ids(self) -> tuple[str, ...]:
        """
        Immutable collection of registered Kāṇḍa IDs.
        """

        return tuple(
            sorted(self._kanda_index.keys())
        )

    # ---------------------------------------------------------
    # Lookup Utilities
    # ---------------------------------------------------------

    def find_varga(
        self,
        varga_id: str,
    ):
        """
        Locate a Varga anywhere in the Amarakośa.
        """

        for kanda in self.kandas:

            varga = kanda.get_varga(varga_id)

            if varga is not None:
                return varga

        return None

    def find_verse(
        self,
        verse_id: str,
    ):
        """
        Locate a Verse anywhere in the Amarakośa.
        """

        for kanda in self.kandas:

            for varga in kanda:

                verse = varga.get_verse(
                    verse_id
                )

                if verse is not None:
                    return verse

        return None

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "edition_id": self.edition_id,

            "title": self.title,

            "author": self.author,

            "language": self.language,

            "script": self.script,

            "version": self.version,

            "source": self.source,

            "editor": self.editor,

            "publisher": self.publisher,

            "publication_year": self.publication_year,

            "notes": self.notes,

            "kanda_count": self.kanda_count,

            "varga_count": self.varga_count,

            "verse_count": self.verse_count,

            "kandas": [

                kanda.to_dict()

                for kanda in self.kandas

            ],
        }

    # ---------------------------------------------------------
    # Python Protocol Methods
    # ---------------------------------------------------------

    def __len__(self) -> int:

        return self.kanda_count

    def __iter__(self):

        return iter(self.kandas)

    def __contains__(
        self,
        kanda_id: str,
    ) -> bool:

        return kanda_id in self._kanda_index

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:

        return self.title

    def __repr__(self) -> str:

        return (
            "Amarakosha("
            f"title='{self.title}', "
            f"kandas={self.kanda_count}, "
            f"vargas={self.varga_count}, "
            f"verses={self.verse_count})"
        )
