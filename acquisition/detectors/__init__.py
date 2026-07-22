
"""
SanskritAI
==========

Acquisition Detectors

Detectors identify properties of acquired resources.

Examples
--------
    • SourceFormatDetector
    • EncodingDetector
    • LanguageDetector

Detectors are intentionally lightweight and stateless.

Version
-------
v0.5.0
"""

from .source_format_detector import SourceFormatDetector

__all__ = [
    "SourceFormatDetector",
]
