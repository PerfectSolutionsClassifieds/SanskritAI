from __future__ import annotations

"""
SanskritAI
==========

Tokenizer Interface

Defines the canonical contract for transforming raw textual
sources into a TokenizationResult.

The tokenizer is the first stage of the SanskritAI language
processing pipeline.

Pipeline
--------

Raw Text
    ↓
Tokenizer
    ↓
TokenizationResult
    ↓
TokenStream
    ↓
Parser

Version
-------
v0.6.0
"""

from abc import ABC, abstractmethod
from typing import Iterable


class Tokenizer(ABC):
    """
    Abstract tokenizer interface.

    A tokenizer converts raw textual input into a
    TokenizationResult.
    """

    @abstractmethod
    def tokenize(
        self,
        source: str,
    ) -> "TokenizationResult":
        """
        Tokenize a single source string.
        """
        raise NotImplementedError

    @abstractmethod
    def tokenize_many(
        self,
        sources: Iterable[str],
    ) -> Iterable["TokenizationResult"]:
        """
        Tokenize multiple source strings.
        """
        raise NotImplementedError

    @abstractmethod
    def supports(
        self,
        source: object,
    ) -> bool:
        """
        Returns True if this tokenizer can process the supplied
        source.
        """
        raise NotImplementedError


# ------------------------------------------------------------------
# Deferred import (avoids circular imports)
# ------------------------------------------------------------------

from SanskritAI.core.tokenizers.tokenization_result import (
    TokenizationResult,
)
