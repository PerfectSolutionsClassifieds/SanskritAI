from __future__ import annotations

"""
SanskritAI
==========

Lexical Dictionary Source

Compatibility enum identifying the dictionary/resource from
which a lexical record originated.

Version
-------
v0.4.1
"""

from enum import Enum


class DictionarySource(str, Enum):
    """
    Canonical lexical source identifiers.
    """

    UNKNOWN = "unknown"

    MONIER_WILLIAMS = "monier_williams"

    APTE = "apte"

    AMARAKOSHA = "amarakosha"

    SHABDAKALPADRUMA = "shabdakalpadruma"

    VACASPATYAM = "vacaspatyam"

    DHATUPATHA = "dhatupatha"

    GANAPATHA = "ganapatha"

    UNADI = "unadi"
