
"""
SanskritAI
==========

Repository Catalog Parsers

Catalog parsers convert repository-specific catalog data (HTML,
XML, JSON, etc.) into CorpusSource domain objects.

Responsibilities
----------------
* Parse repository catalog formats
* Extract corpus metadata
* Produce CorpusSource objects via the factory
* Remain independent of HTTP transport

Concrete Parsers
----------------
* GretilCatalogParser
* CologneCatalogParser
* SaritCatalogParser
* MuktabodhaCatalogParser
* SanskritDocumentsCatalogParser

Catalog parsers intentionally do NOT:

    • perform HTTP requests
    • download corpus files
    • validate resources
    • normalize corpus text
    • import corpora

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .base_catalog_parser import BaseCatalogParser
from .gretil_catalog_parser import GretilCatalogParser

__all__ = [
    "BaseCatalogParser",
    "GretilCatalogParser",
]
