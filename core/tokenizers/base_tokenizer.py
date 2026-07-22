from __future__ import annotations

"""
SanskritAI
==========

Base Tokenizer

Provides reusable infrastructure shared by all tokenizer
implementations.

Responsibilities
----------------
- Source normalization
- Batch tokenization
- Pre-processing hooks
- Post-processing hooks
- Tokenizer metadata

Concrete implementations
------------------------
- SanskritTokenizer
- TeluguTokenizer
- WhitespaceTokenizer
- OCRTokenizer

Pipeline
--------

Raw Text
    ↓
BaseTokenizer
    ↓
Concrete Tokenizer
    ↓
TokenizationResult

Version
-------
v0.6.0
"""

from abc import abstractmethod
from typing import Iterable

from SanskritAI.core.tokenizers.tokenizer import Tokenizer
from SanskritAI.core.tokenizers.tokenization_result import (
    TokenizationResult,
)


class BaseTokenizer(Tokenizer):
    """
    Base implementation shared by all tokenizers.
    """

    def __init__(
        self,
        *,
        name: str | None = None,
        version: str = "1.0",
    ) -> None:
        self._name = name or self.__class__.__name__
        self._version = version

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Human-readable tokenizer name.
        """
        return self._name

    @property
    def version(self) -> str:
        """
        Tokenizer version.
        """
        return self._version

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    def normalize_source(
        self,
        source: str,
    ) -> str:
        """
        Normalize raw input before tokenization.

        Subclasses may override this hook.
        """
        return source

    # ---------------------------------------------------------
    # Processing hooks
    # ---------------------------------------------------------

    def preprocess(
        self,
        source: str,
    ) -> str:
        """
        Hook executed immediately before tokenization.
        """
        return source

    def postprocess(
        self,
        result: TokenizationResult,
    ) -> TokenizationResult:
        """
        Hook executed immediately after tokenization.
        """
        return result

    # ---------------------------------------------------------
    # Batch tokenization
    # ---------------------------------------------------------

    def tokenize_many(
        self,
        sources: Iterable[str],
    ) -> Iterable[TokenizationResult]:
        """
        Tokenize multiple source strings.
        """
        for source in sources:
            normalized = self.normalize_source(source)
            processed = self.preprocess(normalized)
            result = self.tokenize(processed)
            yield self.postprocess(result)

    # ---------------------------------------------------------
    # Capability
    # ---------------------------------------------------------

    def supports(
        self,
        source: object,
    ) -> bool:
        """
        Returns True if this tokenizer supports the supplied
        source.

        Subclasses may override this method for stricter checks.
        """
        return isinstance(source, str)

    # ---------------------------------------------------------
    # Tokenization
    # ---------------------------------------------------------

    @abstractmethod
    def tokenize(
        self,
        source: str,
    ) -> TokenizationResult:
        """
        Tokenize a single source string.

        Concrete subclasses implement the actual tokenization
        algorithm.
        """
        raise NotImplementedError
