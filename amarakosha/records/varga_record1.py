from __future__ import annotations

"""
Canonical parsed Amarakośa Varga.

Produced by parsers.

Consumed by builders.
"""

from dataclasses import dataclass


@dataclass(slots=True,frozen=True)
class VargaRecord:
    """
    Parsed Amarakośa Varga.
    """

    identifier: str

    kanda: str

    varga_number: int

    name: str

    devanagari: str

    iast: str

    title: str

    description: str = ""
