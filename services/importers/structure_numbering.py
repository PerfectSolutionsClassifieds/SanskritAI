
"""
SanskritAI
==========

Module:
    services.importers.structure_numbering

Description
-----------
Parser-independent extractor for structural hierarchy numbering. Isolates 
string indexing rules to allow support for diverse OCR numbering editions later.

Version
-------
v0.5.0-alpha
"""

from __future__ import annotations
from models.amarakosha import Amarakosha, Kanda, Varga


class StructureNumbering:
    """
    Automates sequence calculation for structural elements based on the 
    current status of the object hierarchy graph.
    """

    @staticmethod
    def next_kanda_number(book: Amarakosha) -> int:
        """Determines the chronological index of the incoming Kanda."""
        return len(book.kandas) + 1

    @staticmethod
    def next_varga_number(active_kanda: Kanda | None) -> int:
        """Determines the chronological index of the incoming Varga inside its parent."""
        if active_kanda is None:
            return 1
        return len(active_kanda.vargas) + 1

    @staticmethod
    def next_verse_number(active_varga: Varga | None) -> int:
        """Determines the chronological index of the incoming Verse inside its parent."""
        if active_varga is None:
            return 1
        return len(active_varga.verses) + 1
