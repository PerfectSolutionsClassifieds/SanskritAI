from __future__ import annotations
"""
SanskritAI
==========
Reader Interaction
Domain-level hover and selection semantics for the Reader.
Hover is transient and never changes ReaderSession state or history.
Selection is represented by an immutable ReaderSelectionContext.
Navigation remains the responsibility of ReaderController.
Version
-------
v1.0.0
"""
from dataclasses import dataclass
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_selection_context import ReaderSelectionContext
@dataclass(frozen=True, slots=True)
class ReaderHoverContext:
    """Transient immutable context describing the hovered Reader position."""
    position: ReaderPosition
    @property
    def purana_id(self) -> str:
        return self.position.purana_id
    @property
    def chapter_id(self) -> str | None:
        return self.position.chapter_id
    @property
    def sloka_id(self) -> str | None:
        return self.position.sloka_id
    @property
    def word_id(self) -> str | None:
        return self.position.word_id
    @property
    def level(self) -> str:
        return self.position.level
    @property
    def canonical_id(self) -> str:
        return self.position.canonical_id
    @classmethod
    def from_position(
        cls,
        position: ReaderPosition,
    ) -> "ReaderHoverContext":
        """Create a hover context from a canonical ReaderPosition."""
        return cls(position=position)
    def to_position(self) -> ReaderPosition:
        """Return the canonical ReaderPosition represented by this context."""
        return self.position
    def __str__(self) -> str:
        return str(self.position)
class ReaderInteraction:
    """
    Coordinates transient hover and immutable selection semantics.
    This class does not own navigation, session state, or history.
    """
    @staticmethod
    def hover(
        position: ReaderPosition,
    ) -> ReaderHoverContext:
        """Create transient hover context without changing Reader state."""
        return ReaderHoverContext.from_position(position)
    @staticmethod
    def select(
        position: ReaderPosition,
    ) -> ReaderSelectionContext:
        """Create an immutable selection context."""
        return ReaderSelectionContext.from_position(position)
