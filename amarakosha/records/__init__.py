"""
SanskritAI
==========

Amarakośa Records

Canonical parser output objects.

These immutable records provide a stable interchange format
between parsers, builders and importers.

Version
-------
v0.4.0
"""

from SanskritAI.amarakosha.records.synset_record import (
    SynsetRecord,
)

from SanskritAI.amarakosha.records.varga_record import (
    VargaRecord,
)

__all__ = [
    "SynsetRecord",
    "VargaRecord",
]
