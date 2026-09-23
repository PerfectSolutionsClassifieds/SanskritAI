from __future__ import annotations

"""
SanskritAI
==========

Base Lexical Builder

Abstract base class for all lexical builders.

This class adapts the generic NodeBuilder from the
Architectural Kernel for lexical objects.

NodeBuilder requires two generic parameters:

    NodeBuilder[TNode, TMetadata]

The lexical layer therefore specializes it with the
lexical object's metadata type.

Version
-------
v0.4.1
"""

from abc import ABC
from typing import Any
from typing import Generic

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

    Concrete lexical builders inherit the fluent API supplied
    by NodeBuilder while specializing construction of lexical
    domain objects.

    ``Any`` is intentionally used for the metadata parameter
    at this architectural boundary because individual lexical
    objects may expose different metadata types.

    Concrete builders remain responsible for constructing their
    strongly typed metadata objects.
    """

    pass
