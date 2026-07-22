
"""
SanskritAI
==========

Metadata Extractors

Concrete metadata extractors used by the MetadataManager.

Each extractor is responsible for deriving exactly one category
of metadata from a corpus resource.

Current extractors
------------------
* TitleExtractor

Planned extractors
------------------
* LanguageExtractor
* ScriptExtractor
* CorpusTypeExtractor
* NumberingExtractor
* ChapterExtractor
* WorkIdentifierExtractor
* AuthorExtractor
* PublisherExtractor
* LicenseExtractor

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .title_extractor import TitleExtractor

__all__ = [
    "TitleExtractor",
]
