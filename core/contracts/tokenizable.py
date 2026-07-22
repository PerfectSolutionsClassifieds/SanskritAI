from __future__ import annotations

"""
SanskritAI
==========

Tokenizable Contract

Defines the contract for components capable of producing a
TokenStream from an input source.

Typical implementations include:

- SanskritTokenizer
- Lexer
- Scanner
- XML Tokenizer
- JSON Tokenizer

Architecture
------------

Contract
      │
      ▼
Tokenizable

Version
-------
v0.6.0
"""

from abc import abstractmethod
from typing import Any

from SanskritAI.core.contracts.contract import Contract
from SanskritAI.core.tokenizers.token_stream import TokenStream


class Tokenizable(Contract):
    """
    Contract for tokenizable components.
    """

    @abstractmethod
    def tokenize(
        self,
        source: Any,
    ) -> TokenStream:
        """
        Tokenizes the supplied source.

        Parameters
        ----------
        source:
            Input source to tokenize.

        Returns
        -------
        TokenStream
            Immutable stream of generated tokens.
        """
        raise NotImplementedError
