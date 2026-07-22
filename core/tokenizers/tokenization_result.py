from __future__ import annotations

"""
SanskritAI
==========

Tokenization Result

Represents the canonical outcome of a tokenization operation.

A TokenizationResult encapsulates the generated TokenStream
together with high-level status information. It serves as the
contract between the Tokenizer Kernel and the Parsing Engine.

Future versions may extend this object with diagnostics,
warnings, and performance statistics without changing the
Tokenizer interface.

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

from dataclasses import dataclass, field

from SanskritAI.core.tokenizers.token_stream import TokenStream


@dataclass(slots=True, frozen=True)
class TokenizationResult:
    """
    Immutable result of a tokenization operation.
    """

    # ---------------------------------------------------------
    # Tokenization output
    # ---------------------------------------------------------

    stream: TokenStream = field(default_factory=TokenStream)

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    success: bool = True

    message: str = ""

    # ---------------------------------------------------------
    # Future extension point
    # ---------------------------------------------------------

    diagnostics: tuple[object, ...] = field(default_factory=tuple)

    # ---------------------------------------------------------
    # Convenience properties
    # ---------------------------------------------------------

    @property
    def tokens(self):
        """
        Shortcut to the underlying tokenizer tokens.
        """
        return self.stream.tokens

    @property
    def token_count(self) -> int:
        """
        Total number of tokens produced.
        """
        return len(self.stream)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no tokens were produced.
        """
        return self.stream.is_empty

    @property
    def has_diagnostics(self) -> bool:
        """
        Returns True if diagnostics are present.
        """
        return bool(self.diagnostics)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __bool__(self) -> bool:
        """
        Truthiness reflects tokenization success.
        """
        return self.success

    def __str__(self) -> str:
        return (
            f"TokenizationResult("
            f"success={self.success}, "
            f"tokens={self.token_count})"
        )

    def __repr__(self) -> str:
        return (
            f"TokenizationResult("
            f"stream={self.stream!r}, "
            f"success={self.success!r}, "
            f"message={self.message!r})"
        )
