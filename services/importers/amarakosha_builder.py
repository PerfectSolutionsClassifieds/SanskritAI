
"""
SanskritAI
==========

Module:
    services.importers.amarakosha_builder

Description
-----------
Decoupled Factory Layer for constructing Amarakośa domain models. 
Shields the parser engine from explicit constructors and isolates 
internal structural linking.

Version
-------
v0.5.0-alpha
"""

from __future__ import annotations
from models.amarakosha import Kanda, Varga, Verse


class AmarakoshaBuilder:
    """
    Builder Factory responsible for domain object creation.
    Abstracts constructors away to allow easy metadata expansion later.
    """

    @staticmethod
    def build_kanda(number: int, title: str) -> Kanda:
        """Constructs a clean Kanda domain object instance."""
        return Kanda(
            number=number,
            title=title.strip()
        )

    @staticmethod
    def build_varga(number: int, title: str) -> Varga:
        """Constructs a clean Varga domain object instance."""
        return Varga(
            number=number,
            title=title.strip()
        )

    @staticmethod
    def build_verse(number: int, text: str) -> Verse:
        """Constructs a clean Verse domain object instance."""
        return Verse(
            number=number,
            text=text.strip()
        )
