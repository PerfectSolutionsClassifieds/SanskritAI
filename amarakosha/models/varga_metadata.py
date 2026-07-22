from __future__ import annotations

"""
SanskritAI
==========

Amarakośa Varga Metadata

Metadata describing a Varga (semantic chapter) within one of
the three Kāṇḍas of the Amarakośa.

A Varga groups related Synsets under a common semantic theme.

Version
-------
v0.4.0
"""

from dataclasses import dataclass

from SanskritAI.lexical.models.base_lexical_metadata import (
    BaseLexicalMetadata,
)
from SanskritAI.amarakosha.enums.Amarakanda import (
    Amarakanda,
)


@dataclass(slots=True)
class VargaMetadata(BaseLexicalMetadata):
    """
    Metadata describing an Amarakośa Varga.
    """

    # ---------------------------------------------------------
    # Hierarchy
    # ---------------------------------------------------------

    kanda: Amarakanda = Amarakanda.SVARGADI

    varga_number: int = 0

    # ---------------------------------------------------------
    # Identification
    # ---------------------------------------------------------

    name: str = ""

    devanagari: str = ""

    iast: str = ""

    title: str = ""

    # ---------------------------------------------------------
    # Editorial
    # ---------------------------------------------------------

    description: str = ""

    source_edition: str = ""

    notes: str = ""
