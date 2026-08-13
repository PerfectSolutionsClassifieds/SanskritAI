from __future__ import annotations

"""
SanskritAI
==========

Reader Session History

Purpose
-------
Maintains browser-like navigation history for ReaderSession.

The history layer is deliberately kept separate from:

    ReaderPosition
    ReaderNavigator
    ReaderEngine
    ReaderSession

Responsibilities
----------------
ReaderSessionHistory is responsible only for:

    • recording visited ReaderPosition objects
    • moving backward through history
    • moving forward through history
    • exposing history state
    • preventing redundant consecutive entries
    • clearing forward history after a new navigation

It does NOT:

    • resolve corpus objects
    • perform chapter/sloka/word navigation
    • know anything about Corpus
    • know anything about ReaderRepository
    • mutate ReaderPosition

Navigation model
----------------

                    record()
                       │
                       ▼
                ┌─────────────┐
                │   Current   │
                └─────────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
            back()           record()
              │                 │
              ▼                 ▼
        previous entry     clears forward
              │
              ▼
          forward()

The class stores positions, not corpus objects.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.reader.reader_position import (
    ReaderPosition,
)


@dataclass
class ReaderSessionHistory:
    """
    Browser-style navigation history for ReaderSession.

    The history contains immutable ReaderPosition objects.

    Internal representation
    -----------------------

        _back_stack
        _current
        _forward_stack

    Example
    -------

        record(A)
        record(B)
        record(C)

        back()
            -> B

        back()
            -> A

        forward()
            -> B

        record(D)

        forward()
            -> None

    Recording a new position after going backward clears the
    forward history, matching normal browser navigation semantics.
    """

    _back_stack: list[ReaderPosition] = field(
        default_factory=list,
        repr=False,
    )

    _current: ReaderPosition | None = field(
        default=None,
        repr=False,
    )

    _forward_stack: list[ReaderPosition] = field(
        default_factory=list,
        repr=False,
    )

    # =========================================================
    # Current Position
    # =========================================================

    @property
    def current(
        self,
    ) -> ReaderPosition | None:
        """
        Return the current reader position.
        """

        return self._current

    @property
    def position(
        self,
    ) -> ReaderPosition | None:
        """
        Alias for current.

        Useful when ReaderSession exposes history state as its
        current reader position.
        """

        return self._current

    @property
    def has_current(
        self,
    ) -> bool:
        """
        Return True when a current position exists.
        """

        return self._current is not None

    # =========================================================
    # Backward Navigation
    # =========================================================

    @property
    def can_go_back(
        self,
    ) -> bool:
        """
        Return True when backward navigation is possible.
        """

        return bool(self._back_stack)

    @property
    def can_back(
        self,
    ) -> bool:
        """
        Alias for can_go_back.
        """

        return self.can_go_back

    # =========================================================
    # Forward Navigation
    # =========================================================

    @property
    def can_go_forward(
        self,
    ) -> bool:
        """
        Return True when forward navigation is possible.
        """

        return bool(self._forward_stack)

    @property
    def can_forward(
        self,
    ) -> bool:
        """
        Alias for can_go_forward.
        """

        return self.can_go_forward

    # =========================================================
    # History Sizes
    # =========================================================

    @property
    def back_count(
        self,
    ) -> int:
        """
        Number of positions available through back().
        """

        return len(self._back_stack)

    @property
    def forward_count(
        self,
    ) -> int:
        """
        Number of positions available through forward().
        """

        return len(self._forward_stack)

    @property
    def history_count(
        self,
    ) -> int:
        """
        Total number of positions represented by the history.

        Includes the current position when one exists.
        """

        return (
            len(self._back_stack)
            + (1 if self._current is not None else 0)
            + len(self._forward_stack)
        )

    # =========================================================
    # Recording
    # =========================================================

    def record(
        self,
        position: ReaderPosition,
    ) -> ReaderPosition:
        """
        Record a newly navigated position.

        Behaviour
        ---------
        If there is no current position, the supplied position
        becomes current.

        If the supplied position is identical to the current
        position, nothing is added.

        Otherwise:

            current → back stack
            new position → current
            forward stack → cleared

        Returns
        -------
        ReaderPosition
            The new current position.
        """

        if not isinstance(
            position,
            ReaderPosition,
        ):
            raise TypeError(
                "ReaderSessionHistory accepts only "
                "ReaderPosition instances."
            )

        if self._current == position:
            return self._current

        if self._current is not None:
            self._back_stack.append(
                self._current
            )

        self._current = position

        # A new navigation creates a new branch.
        self._forward_stack.clear()

        return position

    # =========================================================
    # Back
    # =========================================================

    def back(
        self,
    ) -> ReaderPosition | None:
        """
        Move one step backward.

        Returns
        -------
        ReaderPosition | None
            The new current position.

        Boundary
        --------
        If no backward position exists, the current position is
        unchanged and None is returned.
        """

        if not self._back_stack:
            return None

        if self._current is not None:
            self._forward_stack.append(
                self._current
            )

        self._current = self._back_stack.pop()

        return self._current

    # =========================================================
    # Forward
    # =========================================================

    def forward(
        self,
    ) -> ReaderPosition | None:
        """
        Move one step forward.

        Returns
        -------
        ReaderPosition | None
            The new current position.

        Boundary
        --------
        If no forward position exists, the current position is
        unchanged and None is returned.
        """

        if not self._forward_stack:
            return None

        if self._current is not None:
            self._back_stack.append(
                self._current
            )

        self._current = self._forward_stack.pop()

        return self._current

    # =========================================================
    # Peek
    # =========================================================

    @property
    def previous(
        self,
    ) -> ReaderPosition | None:
        """
        Return the position that back() would visit.

        Does not modify history.
        """

        if not self._back_stack:
            return None

        return self._back_stack[-1]

    @property
    def next(
        self,
    ) -> ReaderPosition | None:
        """
        Return the position that forward() would visit.

        Does not modify history.
        """

        if not self._forward_stack:
            return None

        return self._forward_stack[-1]

    # =========================================================
    # Clear
    # =========================================================

    def clear(
        self,
    ) -> None:
        """
        Clear all navigation history.

        After clearing, there is no current position.
        """

        self._back_stack.clear()
        self._forward_stack.clear()
        self._current = None

    def clear_forward(
        self,
    ) -> None:
        """
        Clear only the forward navigation branch.
        """

        self._forward_stack.clear()

    # =========================================================
    # State
    # =========================================================

    @property
    def is_empty(
        self,
    ) -> bool:
        """
        Return True when the history contains no position.
        """

        return (
            self._current is None
            and not self._back_stack
            and not self._forward_stack
        )

    # =========================================================
    # Display
    # =========================================================

    @property
    def display_name(
        self,
    ) -> str:
        return "Reader Session History"

    @property
    def display_text(
        self,
    ) -> str:

        if self._current is None:
            return "Reader history is empty"

        return str(self._current)

    @property
    def display_description(
        self,
    ) -> str:

        return (
            f"{self.back_count} back, "
            f"{self.forward_count} forward"
        )

    # =========================================================
    # String Representation
    # =========================================================

    def __str__(
        self,
    ) -> str:
        return self.display_text
