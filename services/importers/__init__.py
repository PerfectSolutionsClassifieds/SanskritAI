"""
SanskritAI
==========

Import Services

Provides corpus import infrastructure for SanskritAI.

Architecture
------------

Importer
    │
    ▼
Parser
    │
    ▼
Domain Model
    │
    ▼
ImportResult

Importers
---------

AmarakoshaImporter
    High-level Amarakośa import workflow.

AmarakoshaParser
    Converts Amarakośa text into the canonical
    Amarakosha domain model.

Future Modules
--------------

    parser_state.py
    line_classifier.py
    unicode_normalizer.py
    parser_context.py

Future Importers
----------------

    ShivaPuranaImporter
    DeviBhagavataImporter
    MahabharataImporter
    RamayanaImporter
    RigvedaImporter

Version:
    v0.4.0
"""

from .amarakosha_importer import AmarakoshaImporter
from .amarakosha_parser import AmarakoshaParser

__all__ = [
    "AmarakoshaImporter",
    "AmarakoshaParser",
]
