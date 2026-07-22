from __future__ import annotations

"""
SanskritAI
==========

SupportsProcessing Protocol

Defines the structural protocol for processable components.

Unlike semantic Contracts, this protocol specifies only the
required structural interface and enables structural typing
(PEP 544).

This protocol intentionally avoids depending on concrete
processing implementations, allowing it to support parsers,
tokenizers, analyzers, transformers, importers, AI pipelines,
and other processing components.

Typical implementations include:

- Parser
- Tokenizer
- Morphological Analyzer
- Sandhi Engine
- Compound Analyzer
- Import Pipeline
- AI Processing Pipeline

Architecture
------------

Protocol
      │
      ▼
SupportsProcessing

Version
-------
v0.6.0
"""

from typing import Generic
from typing import TypeVar
from typing import runtime_checkable

from SanskritAI.core.protocols.protocol import Protocol

I = TypeVar("I")  # Input type
R = TypeVar("R")  # Processing result type


@runtime_checkable
class SupportsProcessing(Protocol, Generic[I, R]):
    """
    Structural protocol for processing components.
    """

    def process(
        self,
        value: I,
    ) -> R:
        """
        Processes the supplied input value.
        """
        ...
