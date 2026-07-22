
"""
SanskritAI
==========

Metadata Extraction Framework

This package provides reusable metadata extraction services for
corpus resources.

Metadata extraction is intentionally independent from:

    • discovery
    • downloading
    • validation
    • normalization
    • importing

Typical metadata includes:

    • work title
    • corpus type
    • language
    • writing script
    • numbering scheme
    • chapter hierarchy
    • repository identifiers

Version
-------
v0.5.0
"""

from .base_metadata_extractor import BaseMetadataExtractor
from .extraction_result import ExtractionResult
from .metadata_manager import MetadataManager

__all__ = [
    "BaseMetadataExtractor",
    "ExtractionResult",
    "MetadataManager",
]
