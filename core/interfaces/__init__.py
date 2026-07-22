"""
SanskritAI
==========

Core Interfaces

Abstract contracts shared throughout the SanskritAI
Architectural Kernel.

Interfaces define behaviour without prescribing
implementation, allowing individual subsystems to
remain loosely coupled.

Available Interfaces
--------------------

Identifiable
Serializable
Hierarchical
Builder
Repository

Version
-------
v0.3.0
"""

from .identifiable import Identifiable
from .serializable import Serializable
from .hierarchical import Hierarchical
from .builder import Builder
from .repository import Repository

__all__ = [
    "Identifiable",
    "Serializable",
    "Hierarchical",
    "Builder",
    "Repository",
]
