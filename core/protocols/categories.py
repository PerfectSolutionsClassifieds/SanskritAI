from __future__ import annotations

"""
SanskritAI
==========

Protocol Categories

Defines the architectural classification of structural
protocols used throughout the SanskritAI framework.

Protocols are grouped by structural complexity rather than
functional domain.

Architecture
------------

Foundational Protocols
    • Protocol
    • SupportsIteration
    • SupportsLookup

Collection Protocols
    • SupportsRegistry
    • SupportsSearch

Behavioral Protocols
    • SupportsSerialization
    • SupportsProcessing

This module exists primarily for documentation,
classification, and future introspection.

Version
-------
v0.6.0
"""

from enum import Enum


class ProtocolCategory(str, Enum):
    """
    Canonical protocol categories.
    """

    FOUNDATIONAL = "foundational"

    COLLECTION = "collection"

    BEHAVIORAL = "behavioral"

    INFRASTRUCTURE = "infrastructure"
