
from __future__ import annotations

"""
SanskritAI
==========

Lexical Dictionary Source Enumeration
=====================================

Defines the canonical dictionary/source identifiers used by
LexemeRecord.

Version
-------
v0.4.2
"""

from enum import Enum


class DictionarySource(
    str,
    Enum,
):
    """
    Canonical lexical dictionary/source identifiers.
    """

    UNKNOWN = "unknown"

    MONIER_WILLIAMS = "monier-williams"

    APTE = "apte"

    AMARAKOSHA = "amarakosha"

    SHABDAKALPADRUMA = "shabdakalpadruma"

    VACASPATYAM = "vacaspatyam"

    DHATUPATHA = "dhatupatha"

    GANAPATHA = "ganapatha"

    UNADI = "unadi"

    @classmethod
    def from_value(
        cls,
        value: str | "DictionarySource",
    ) -> "DictionarySource":
        """
        Convert a textual source identifier into a
        DictionarySource member.
        """

        if isinstance(
            value,
            cls,
        ):
            return value

        normalized = (
            value
            .strip()
            .lower()
            .replace("_", "-")
            .replace("–", "-")
            .replace("—", "-")
        )

        aliases = {
            "mw": cls.MONIER_WILLIAMS,
            "monier-williams": cls.MONIER_WILLIAMS,
            "monier williams": cls.MONIER_WILLIAMS,

            "apte": cls.APTE,

            "amara": cls.AMARAKOSHA,
            "amarakosha": cls.AMARAKOSHA,

            "shabdakalpadruma":
                cls.SHABDAKALPADRUMA,

            "vacaspatyam":
                cls.VACASPATYAM,

            "dhatupatha":
                cls.DHATUPATHA,

            "ganapatha":
                cls.GANAPATHA,

            "unadi":
                cls.UNADI,
        }

        return aliases.get(
            normalized,
            cls.UNKNOWN,
        )
