"""
SanskritAI
==========

Diagnostics Kernel

Provides a unified diagnostics infrastructure shared across all
SanskritAI subsystems.

Subsystems
----------
- Tokenizer
- Parser
- Corpus
- Lexical
- Amarakośa
- Morphology
- Sandhi
- Padaccheda
- Importers
- Validators
- Builders

Pipeline
--------

Subsystem
      ↓
Diagnostic
      ↓
DiagnosticCollection
      ↓
DiagnosticReport

Version
-------
v0.6.0
"""

from .diagnostic_severity import DiagnosticSeverity
from .diagnostic_code import DiagnosticCode
from .diagnostic import Diagnostic
from .diagnostic_collection import DiagnosticCollection
from .diagnostic_report import DiagnosticReport

__all__ = [
    "DiagnosticSeverity",
    "DiagnosticCode",
    "Diagnostic",
    "DiagnosticCollection",
    "DiagnosticReport",
]
