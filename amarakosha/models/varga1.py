from __future__ import annotations

"""
SanskritAI
==========

Amarakośa Varga

Represents a semantic chapter within an Amarakośa Kāṇḍa.

Hierarchy
---------

Amarakanda
    └── Varga
            └── Synset
                    └── Lexeme

Version
-------
v0.4.0
"""

from typing import Iterable

from SanskritAI.corpus.models.container_node import (
    ContainerNode,
)

from SanskritAI.amarakosha.models.synset import (
    Synset,
)
from SanskritAI.amarakosha.models.varga_metadata import (
    VargaMetadata,
)


class Varga(
    ContainerNode[
        str,
        VargaMetadata,
        Synset,
    ]
):
    """
    Amarakośa semantic chapter.
    """

    def __init__(
        self,
        identifier: str,
        metadata: VargaMetadata,
        children: Iterable[Synset] | None = None,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
            children=children,
        )

    # ---------------------------------------------------------

    @property
    def synsets(self):
        """
        Iterate over the synsets contained in this varga.
        """
        return iter(self.children)

    # ---------------------------------------------------------

    @property
    def kanda(self):
        """
        Parent Kāṇḍa.
        """
        return self.metadata.kanda

    @property
    def varga_number(self) -> int:
        """
        Canonical ordering within the Kāṇḍa.
        """
        return self.metadata.varga_number

    @property
    def name(self) -> str:
        """
        Traditional varga name.
        """
        return self.metadata.name

    @property
    def title(self) -> str:
        """
        Human-readable title.
        """
        return self.metadata.title

    # ---------------------------------------------------------

    def add_synset(
        self,
        synset: Synset,
    ) -> None:
        """
        Add a synset to this varga.
        """
        self.add_child(synset)

    # ---------------------------------------------------------

    def remove_synset(
        self,
        synset: Synset,
    ) -> None:
        """
        Remove a synset from this varga.
        """
        self.remove_child(synset)
