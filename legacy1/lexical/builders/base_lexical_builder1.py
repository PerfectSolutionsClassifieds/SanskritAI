from __future__ import annotations

"""
SanskritAI
==========

Base Lexical Builder

Abstract base class for all lexical builders.

This class adapts the generic NodeBuilder from the
Architectural Kernel for lexical objects.

Version
-------
v0.3.0
"""

from abc import ABC
from typing import Generic

from SanskritAI.core.typing import (
    TObject,
)

from SanskritAI.corpus.builders.node_builder import (
    NodeBuilder,
)


class BaseLexicalBuilder(
    NodeBuilder[TObject],
    Generic[TObject],
    ABC,
):
    """
    Base class for lexical builders.

    Concrete builders inherit the fluent API provided by
    NodeBuilder while specializing construction of lexical
    domain objects.
    """

    pass
