
"""
SanskritAI
==========

Corpus Discovery Providers

Discovery providers locate available Sanskrit corpus resources
from various repositories.

Each provider is responsible for one source of corpus metadata.

Examples
--------
    • LocalDirectoryProvider
    • GRETILProvider
    • CologneProvider
    • SARITProvider
    • MuktabodhaProvider
    • SanskritDocumentsProvider

Providers intentionally do NOT:

    • download resources
    • validate files
    • normalize content
    • import corpora

Those responsibilities belong to later acquisition stages.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .local_directory_provider import LocalDirectoryProvider

__all__ = [
    "LocalDirectoryProvider",
]
