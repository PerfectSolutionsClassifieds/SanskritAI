from __future__ import annotations

"""
SanskritAI
==========

Parser Cursor

Provides mutable navigation over an immutable TokenStream.

ParserCursor encapsulates all parser state, allowing parsers
to remain stateless and focused exclusively on grammar.

Responsibilities
----------------
- Cursor navigation
- Look-ahead
- Consumption
- Mark / Restore
- End-of-stream detection

Version
-------
v0.6.0
"""

from collections.abc import Iterator

from SanskritAI.core.parsers.cursor.cursor_exception import (
    CursorException,
)
from SanskritAI.core.parsers.cursor.cursor_mark import (
    CursorMark,
)
from SanskritAI.core.parsers.cursor.cursor_state import (
    CursorState,
)
from SanskritAI.core.tokenizers.token_stream import (
    TokenStream,
)
from SanskritAI.core.tokenizers.tokenizer_token import (
    TokenizerToken,
)


class ParserCursor:
    """
    Mutable navigation object over an immutable TokenStream.
    """

    def __init__(
        self,
        stream: TokenStream,
    ) -> None:
        self._stream = stream
        self._state = CursorState()

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def stream(self) -> TokenStream:
        return self._stream

    @property
    def state(self) -> CursorState:
        return self._state

    @property
    def index(self) -> int:
        return self._state.index

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def eof(self) -> bool:
        """
        Returns True when the cursor is positioned beyond the
        last token.
        """
        return self.index >= len(self._stream)

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def current(self) -> TokenizerToken | None:
        """
        Current token.
        """
        if self.eof():
            return None

        return self._stream[self.index]

    def peek(
        self,
        offset: int = 1,
    ) -> TokenizerToken | None:
        """
        Look ahead without advancing.
        """
        position = self.index + offset

        if position >= len(self._stream):
            return None

        return self._stream[position]

    def previous(self) -> TokenizerToken | None:
        """
        Previous token.
        """
        if self.index == 0:
            return None

        return self._stream[self.index - 1]

    def advance(
        self,
        count: int = 1,
    ) -> TokenizerToken | None:
        """
        Advance the cursor.

        Returns the new current token.
        """
        self._state = self._state.advance(count)

        return self.current()

    def consume(self) -> TokenizerToken:
        """
        Consume the current token and advance.
        """
        token = self.current()

        if token is None:
            raise CursorException(
                "Cannot consume past end of stream.",
                index=self.index,
            )

        self.advance()

        return token

    # ---------------------------------------------------------
    # Mark / Restore
    # ---------------------------------------------------------

    def mark(
        self,
        label: str = "",
    ) -> CursorMark:
        """
        Create a checkpoint.
        """
        return CursorMark(
            index=self.index,
            label=label,
        )

    def restore(
        self,
        mark: CursorMark,
    ) -> None:
        """
        Restore a previous checkpoint.
        """
        self._state = CursorState(
            index=mark.index,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset to the beginning of the stream.
        """
        self._state = CursorState()

    def remaining(self) -> int:
        """
        Number of remaining tokens.
        """
        return max(0, len(self._stream) - self.index)

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(self) -> Iterator[TokenizerToken]:
        while not self.eof():
            yield self.consume()

    def __len__(self) -> int:
        return len(self._stream)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(index={self.index}, "
            f"remaining={self.remaining()})"
        )
