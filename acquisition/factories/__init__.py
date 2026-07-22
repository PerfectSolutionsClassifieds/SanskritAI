
"""
SanskritAI
==========

Acquisition Factories

Factories are responsible for constructing acquisition domain
objects from raw discovery metadata.

Responsibilities
----------------
* Construct CorpusSource instances
* Encapsulate object creation logic
* Provide reusable creation APIs

Factories intentionally do NOT:

    • discover resources
    • download files
    • validate content
    • normalize text
    • parse corpora

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .corpus_source_factory import CorpusSourceFactory

__all__ = [
    "CorpusSourceFactory",
]
