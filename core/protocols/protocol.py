from __future__ import annotations

"""
SanskritAI
==========

Base Protocol

Defines the canonical root protocol for all structural typing
protocols used throughout the SanskritAI architecture.

Protocols provide structural compatibility (PEP 544) and enable
dependency inversion without requiring inheritance.

Unlike Contracts, protocols specify the shape of an object
rather than its semantic role.

Architecture
------------

typing.Protocol
        │
        ▼
Protocol
        │
        ├── SupportsLookup
        ├── SupportsRegistry
        ├── SupportsSearch
        ├── SupportsSerialization
        └── SupportsProcessing

Version
-------
v0.6.0
"""

from typing import Protocol as TypingProtocol
from typing import runtime_checkable


@runtime_checkable
class Protocol(TypingProtocol):
    """
    Root protocol for all SanskritAI structural protocols.

    This class intentionally defines no members. It exists only
    to provide a common architectural root for all protocols in
    the SanskritAI framework.
    """

    __slots__ = ()
