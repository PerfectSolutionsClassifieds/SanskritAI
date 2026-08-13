from __future__ import annotations
"""SanskritAI
============
Reader Selection Context
Immutable context describing the currently selected Reader object.
ReaderSelectionContext does not perform navigation, resolution, or history
management. Those responsibilities remain with ReaderNavigator,
ReaderEngine, and ReaderSession.
Hierarchy
---------
ReaderPosition
    ↓
ReaderSelectionContext
    ├── purāṇa
    ├── chapter
    ├── śloka
    └── word
Version
-------
v1.0.0
"""
from dataclasses import dataclass
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.reader.reader_position import ReaderPosition
@dataclass(frozen=True, slots=True)
class ReaderSelectionContext(ValueObject, Immutable, Displayable):
    """Immutable description of the currently selected Reader position."""
    position: ReaderPosition
    @property
    def display_name(self) -> str:
        return "Reader Selection Context"
    @property
    def display_text(self) -> str:
        return str(self.position)
    @property
    def display_description(self) -> str:
        return "Immutable context describing the current Reader selection."
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
    @property
    def identifier(self) -> str:
        return self.position.identifier
    @property
    def is_purana(self) -> bool:
        return self.position.is_purana
    @property
    def is_chapter(self) -> bool:
        return self.position.is_chapter
    @property
    def is_sloka(self) -> bool:
        return self.position.is_sloka
    @property
    def is_word(self) -> bool:
        return self.position.is_word
    @property
    def has_chapter(self) -> bool:
        return self.chapter_id is not None
    @property
    def has_sloka(self) -> bool:
        return self.sloka_id is not None
    @property
    def has_word(self) -> bool:
        return self.word_id is not None
    @classmethod
    def from_position(cls, position: ReaderPosition) -> ReaderSelectionContext:
        """Create a selection context from a canonical ReaderPosition."""
        return cls(position=position)
    def to_position(self) -> ReaderPosition:
        """Return the canonical ReaderPosition represented by this context."""
        return self.position
    def __str__(self) -> str:
        return self.display_text
