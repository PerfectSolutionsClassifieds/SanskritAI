
"""
SanskritAI
==========

Acquisition Validators

Provides validation services for acquired corpus resources.

Responsibilities
----------------
The validator subsystem verifies that acquired resources are
complete, trustworthy, and suitable for downstream processing.

Validators may perform tasks such as:

    • File existence verification
    • File size validation
    • Checksum verification
    • Archive integrity checks
    • Encoding detection
    • Structural validation

Validators intentionally do NOT perform:

    • Downloading
    • Unicode normalization
    • Corpus parsing
    • Database importing

Those responsibilities belong to other layers of the
acquisition framework.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from .base_validator import BaseValidator
from .checksum_validator import ChecksumValidator
from .file_validator import FileValidator

__all__ = [
    "BaseValidator",
    "ChecksumValidator",
    "FileValidator",
]
