from __future__ import annotations

"""
SanskritAI
==========

Amarakośa Registry

Central registry for Amarakośa knowledge objects.

Version
-------
v0.4.0
"""

from typing import Iterable

from SanskritAI.core.registries.base_registry import BaseRegistry

from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.models.varga import Varga


class AmarakoshaRegistry(
    BaseRegistry[str, object],
):
    """
    Registry for Amarakośa knowledge objects.
    """

    def register_many(
        self,
        objects: Iterable[object],
    ) -> None:

        for obj in objects:
            self.register(obj)

    # ---------------------------------------------------------

    def vargas(self):

        for obj in self.values():
            if isinstance(obj, Varga):
                yield obj

    # ---------------------------------------------------------

    def synsets(self):

        for obj in self.values():
            if isinstance(obj, Synset):
                yield obj
