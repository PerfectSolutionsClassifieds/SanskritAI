
from __future__ import annotations

"""
SanskritAI
==========

Base Lexical Builder
====================

Abstract adapter between the generic corpus ``NodeBuilder`` and
the lexical domain builders.

The architectural ``NodeBuilder`` is parameterized by:

    NodeBuilder[TNode, TMetadata]

Lexical builders specialize only the domain object type here while
using ``Any`` for the generic metadata parameter because concrete
lexical builders own their domain-specific metadata construction.

Version
-------
v0.4.2
"""

from abc import ABC
from typing import Any, Generic

from SanskritAI.core.typing import (
    TObject,
)

from SanskritAI.corpus.builders.node_builder import (
    NodeBuilder,
)


class BaseLexicalBuilder(
    NodeBuilder[TObject, Any],
    Generic[TObject],
    ABC,
):
    """
    Base class for lexical builders.

    This class adapts the generic corpus ``NodeBuilder`` to the
    lexical subsystem without introducing a second lexical metadata
    hierarchy.

    Concrete lexical builders provide their own construction logic
    and metadata representation.
    """

    pass
