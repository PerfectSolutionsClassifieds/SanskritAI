"""
SanskritAI
==========

Module:
    models.amarakosha.kanda

Description
-----------
Represents one Kāṇḍa (major division) of the Amarakośa.

A Kāṇḍa contains an ordered collection of Vargas.

Examples
--------
    1. Svargādikāṇḍa
    2. Bhūvargādikāṇḍa
    3. Sāmānyādikāṇḍa

This class represents only the canonical domain model.

No parsing, importing, searching, or repository logic belongs here.

Version:
    v0.4.0
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .varga import Varga


@dataclass(slots=True)
class Kanda:
    """
    Represents one Amarakośa Kāṇḍa.

    Structure
    ---------

    Kāṇḍa

        ├── Varga

        ├── Varga

        └── Varga
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    kanda_id: str

    kanda_number: int

    title: str

    # ---------------------------------------------------------
    # Optional Metadata
    # ---------------------------------------------------------

    english_title: str = ""

    description: str = ""

    notes: str = ""

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------

    vargas: list[Varga] = field(default_factory=list)

    # ---------------------------------------------------------
    # Internal Index
    # ---------------------------------------------------------

    _varga_index: dict[str, Varga] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def __post_init__(self) -> None:

        self.kanda_id = self.kanda_id.strip()

        self.title = self.title.strip()

        if not self.kanda_id:
            raise ValueError(
                "kanda_id cannot be empty."
            )

        if self.kanda_number <= 0:
            raise ValueError(
                "kanda_number must be positive."
            )

        if not self.title:
            raise ValueError(
                "title cannot be empty."
            )

        for varga in self.vargas:
            self._varga_index[varga.varga_id] = varga

    # ---------------------------------------------------------
    # Varga Operations
    # ---------------------------------------------------------

    def add_varga(
        self,
        varga: Varga,
    ) -> None:
        """
        Add or replace a Varga.
        """

        existing = self._varga_index.get(
            varga.varga_id
        )

        if existing is not None:

            index = self.vargas.index(existing)

            self.vargas[index] = varga

        else:

            self.vargas.append(varga)

        self._varga_index[
            varga.varga_id
        ] = varga

    def get_varga(
        self,
        varga_id: str,
    ) -> Varga | None:

        return self._varga_index.get(varga_id)

    def remove_varga(
        self,
        varga_id: str,
    ) -> bool:

        varga = self._varga_index.pop(
            varga_id,
            None,
        )

        if varga is None:
            return False

        self.vargas.remove(varga)

        return True

    def clear(self) -> None:

        self.vargas.clear()

        self._varga_index.clear()

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    @property
    def varga_count(self) -> int:

        return len(self.vargas)

    @property
    def verse_count(self) -> int:
        """
        Total verses contained in this Kāṇḍa.
        """

        return sum(
            varga.verse_count
            for varga in self.vargas
        )

    @property
    def first_varga(self) -> Varga | None:

        if not self.vargas:
            return None

        return self.vargas[0]

    @property
    def last_varga(self) -> Varga | None:

        if not self.vargas:
            return None

        return self.vargas[-1]

    @property
    def varga_ids(self) -> tuple[str, ...]:
        """
        Immutable collection of registered Varga IDs.
        """

        return tuple(
            sorted(self._varga_index.keys())
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "kanda_id": self.kanda_id,

            "kanda_number": self.kanda_number,

            "title": self.title,

            "english_title": self.english_title,

            "description": self.description,

            "notes": self.notes,

            "varga_count": self.varga_count,

            "verse_count": self.verse_count,

            "vargas": [

                varga.to_dict()

                for varga in self.vargas

            ],
        }

    # ---------------------------------------------------------
    # Python Protocol Methods
    # ---------------------------------------------------------

    def __len__(self) -> int:

        return self.varga_count

    def __iter__(self):

        return iter(self.vargas)

    def __contains__(
        self,
        varga_id: str,
    ) -> bool:

        return varga_id in self._varga_index

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:

        return self.title

    def __repr__(self) -> str:

        return (
            "Kanda("
            f"id='{self.kanda_id}', "
            f"number={self.kanda_number}, "
            f"title='{self.title}', "
            f"vargas={self.varga_count}, "
            f"verses={self.verse_count})"
        )
