"""
SanskritAI
==========

Core Architectural Kernel

The ``core`` package contains the reusable framework
infrastructure shared across every subsystem of SanskritAI.

Subpackages
-----------
interfaces/
builders/
registries/
factories/
events/
mixins/

This package intentionally contains no Sanskrit-specific
business logic. It provides the architectural foundation
upon which higher-level modules are built.

Version
-------
v0.3.0
"""

__version__ = "0.3.0"

__all__ = [
    "__version__",
]
