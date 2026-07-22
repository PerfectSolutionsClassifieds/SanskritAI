
"""
SanskritAI
==========

Acquisition Normalizers

Provides normalization services for acquired corpus resources.

Responsibilities
----------------
Normalizers transform acquired resources into a consistent,
canonical representation before they are parsed or imported.

Typical normalization tasks include:

    • Unicode normalization
    • Line-ending normalization
    • Whitespace normalization
    • Removal of invisible Unicode characters
    • Canonical text formatting

Normalizers intentionally do NOT perform:

    • Downloading
    • Validation
    • Corpus parsing
    • Linguistic analysis
    • Database importing

These responsibilities belong to other layers of the
acquisition framework.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .base_normalizer import BaseNormalizer
from .composite_normalizer import CompositeNormalizer
from .unicode_normalizer import UnicodeNormalizer
from .sanskrit_normalizer import SanskritNormalizer
from .line_ending_normalizer import LineEndingNormalizer
from .whitespace_normalizer import WhitespaceNormalizer

__all__ = [
    "BaseNormalizer",
    "CompositeNormalizer",
    "UnicodeNormalizer",
    "SanskritNormalizer",
    "LineEndingNormalizer",
    "WhitespaceNormalizer",
]
