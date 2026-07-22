from __future__ import annotations

"""
SanskritAI
==========

Processable Contract

Defines the architectural contract for components that
participate in the SanskritAI processing pipeline.

Processing is a broad architectural capability encompassing
parsing, tokenization, morphological analysis, sandhi
analysis, compound analysis, syntactic analysis, semantic
analysis, indexing, and future AI workflows.

This contract intentionally specifies *what* a processing
component must provide without prescribing the underlying
processing algorithm or result type.

Typical implementations include:

- Parser
- Tokenizer
- MorphologicalEngine
- SandhiEngine
- SamasaEngine
- SyntaxEngine
- SemanticEngine
- Corpus Import Pipeline
- AI Processing Pipeline

Architecture
------------

Contract
      │
      ▼
Processable

Version
-------
v0.6.0
"""

from abc import abstractmethod
from typing import Any

from SanskritAI.core.contracts.contract import Contract


class Processable(Contract):
    """
    Architectural contract for processing components.
    """

    @abstractmethod
    def process(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Executes the processing operation.

        The concrete implementation determines the accepted
        input, processing strategy, and result type.
        """
        raise NotImplementedError

    @property
    def can_process(self) -> bool:
        """
        Indicates that this component supports processing.
        """
        return True

    @property
    def processor_name(self) -> str:
        """
        Returns the canonical processor name.
        """
        return self.__class__.__name__

    @property
    def processor_type(self) -> type:
        """
        Returns the concrete processor type.
        """
        return type(self)
