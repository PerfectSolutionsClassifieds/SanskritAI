from __future__ import annotations

"""
SanskritAI
==========

Base Amarakośa Builder

Abstract base class for all Amarakośa builders.

Version
-------
v0.4.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.typing import TObject
from SanskritAI.corpus.builders.node_builder import NodeBuilder


class BaseAmarakoshaBuilder(
    NodeBuilder[TObject],
    Generic[TObject],
    ABC,
):
    """
    Base class for Amarakośa builders.
    """

    pass
