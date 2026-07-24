"""
SanskritAI
==========

Version Kernel

Provides immutable value objects for representing versions and
version constraints throughout the SanskritAI framework.

Architecture
------------

Version
    │
    ├── SemanticVersion
    └── VersionConstraint
"""

from SanskritAI.core.version.version import Version
from SanskritAI.core.version.semantic_version import SemanticVersion
from SanskritAI.core.version.version_constraint import VersionConstraint

__all__ = [
    "Version",
    "SemanticVersion",
    "VersionConstraint",
]
