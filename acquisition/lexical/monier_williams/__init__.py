"""
SanskritAI
==========

Monier-Williams Acquisition Layer
"""

from .delimited_monier_williams_parser import (
    DelimitedMonierWilliamsParser,
)
from .file_monier_williams_source import (
    FileMonierWilliamsSource,
)
from .monier_williams_acquisition_service import (
    MonierWilliamsAcquisitionService,
)
from .monier_williams_parser import (
    MonierWilliamsParser,
)
from .monier_williams_source import (
    MonierWilliamsSource,
)

__all__ = [
    "DelimitedMonierWilliamsParser",
    "FileMonierWilliamsSource",
    "MonierWilliamsAcquisitionService",
    "MonierWilliamsParser",
    "MonierWilliamsSource",
]
