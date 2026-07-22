from __future__ import annotations

"""
SanskritAI
==========

Varga Builder

Fluent builder for Amarakośa Varga objects.

Version
-------
v0.4.0
"""

from SanskritAI.amarakosha.builders.base_amarakosha_builder import (
    BaseAmarakoshaBuilder,
)
from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.models.varga import Varga
from SanskritAI.amarakosha.models.varga_metadata import (
    VargaMetadata,
)


class VargaBuilder(
    BaseAmarakoshaBuilder[Varga],
):
    """
    Fluent builder for Varga.
    """

    def __init__(self) -> None:
        super().__init__()

        self._identifier = ""
        self._metadata = VargaMetadata()
        self._synsets: list[Synset] = []

    # ---------------------------------------------------------

    def with_identifier(
        self,
        identifier: str,
    ) -> "VargaBuilder":

        self._identifier = identifier
        return self

    # ---------------------------------------------------------

    def with_metadata(
        self,
        metadata: VargaMetadata,
    ) -> "VargaBuilder":

        self._metadata = metadata
        return self

    # ---------------------------------------------------------

    def add_synset(
        self,
        synset: Synset,
    ) -> "VargaBuilder":

        self._synsets.append(synset)
        return self

    # ---------------------------------------------------------

    def build(self) -> Varga:

        return Varga(
            identifier=self._identifier,
            metadata=self._metadata,
            children=self._synsets,
        )
