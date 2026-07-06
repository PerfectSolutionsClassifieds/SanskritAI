"""
SanskritAI
==========

Import Models

Generic import framework shared by all corpus importers.

This package defines the common data structures used by
importers throughout SanskritAI.

Modules
-------

ImportConfiguration
    Controls importer behaviour.

ImportStatus
    Standard lifecycle of an import.

ImportError
    Structured diagnostic information.

ImportStatistics
    Metrics collected during import.

ImportResult
    Complete result returned by every importer.

These classes are intentionally independent of any specific
corpus and can therefore be reused by:

    • Amarakośa
    • Purāṇas
    • Vedas
    • Dictionaries
    • XML/JSON importers
    • OCR pipelines
    • Future SanskritAI datasets

Version:
    v0.4.0
"""

from .import_configuration import ImportConfiguration
from .import_error import ImportError
from .import_result import ImportResult
from .import_statistics import ImportStatistics
from .import_status import ImportStatus

__all__ = [

    "ImportConfiguration",

    "ImportError",

    "ImportResult",

    "ImportStatistics",

    "ImportStatus",
]
