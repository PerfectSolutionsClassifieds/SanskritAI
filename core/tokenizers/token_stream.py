from __future__ import annotations

"""
SanskritAI
==========

Token Stream

Immutable sequence of TokenizerToken objects produced by the
Tokenizer Kernel.

A TokenStream provides a parser-friendly view over a sequence
of tokens while remaining independent of any parsing strategy.

Pipeline
--------

Raw Text
    ↓
Tokenizer
    ↓
TokenStream
    ↓
Parser

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.tokenizers.tokenizer_token import (
    TokenizerToken,
)


@dataclass(slots=True, frozen=True)
class TokenStream:
    """
    Immutable sequence of tokenizer tokens.
    """

    tokens: tuple[TokenizerToken, ...] = field(
        default_factory=tuple
    )

    @property
    def size(self) -> int:
        """
        Number of tokens in the stream.
        """
        return len(self.tokens)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if the stream contains no tokens.
        """
        return not self.tokens

    @property
    def first(self) -> TokenizerToken | None:
        """
        First token in the stream.
        """
        return self.tokens[0] if self.tokens else None

    @property
    def last(self) -> TokenizerToken | None:
        """
        Last token in the stream.
        """
        return self.tokens[-1] if self.tokens else None

    def at(
        self,
        index: int,
    ) -> TokenizerToken:
        """
        Return the token at the given index.
        """
        return self.tokens[index]

    def slice(
        self,
        start: int,
        stop: int | None = None,
    ) -> "TokenStream":
        """
        Return a sub-stream.
        """
        return TokenStream(
            tokens=self.tokens[start:stop]
        )

    def __len__(self) -> int:
        return len(self.tokens)

    def __iter__(self) -> Iterator[TokenizerToken]:
        return iter(self.tokens)

    def __getitem__(
        self,
        index: int | slice,
    ):
        if isinstance(index, slice):
            return TokenStream(
                tokens=self.tokens[index]
            )
        return self.tokens[index]

    def __contains__(
        self,
        token: TokenizerToken,
    ) -> bool:
        return token in self.tokens

    def __str__(self) -> str:
        return (
            f"TokenStream(size={self.size})"
        )

    def __repr__(self) -> str:
        return (
            f"TokenStream(tokens={self.tokens!r})"
        )
