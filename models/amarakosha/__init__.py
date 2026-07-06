"""
SanskritAI
==========

Amarakośa Domain Model

Canonical object model representing the complete structure
of the Amarakośa.

Hierarchy
---------

    Amarakosha
        └── Kanda
              └── Varga
                    └── Verse

This package defines only the domain model.

It intentionally excludes:

    • parser logic
    • importer logic
    • repository logic
    • search logic
    • persistence logic

Those responsibilities belong to higher architectural layers.

Version:
    v0.4.0
"""

from .verse import Verse
from .varga import Varga
from .kanda import Kanda
from .amarakosha import Amarakosha

__all__ = [
    "Verse",
    "Varga",
    "Kanda",
    "Amarakosha",
]
