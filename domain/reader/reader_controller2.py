from __future__ import annotations
"""SanskritAI
==========
Reader Controller
Application-facing orchestration façade for ReaderSession.
ReaderController coordinates the active ReaderSession without duplicating
navigation, resolution, or history logic owned by the Reader domain.
Version
-------
v1.0.0
"""
from dataclasses import dataclass
from typing import Any
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_session import ReaderSession
from SanskritAI.domain.reader.reader_document import ReaderDocument
from SanskritAI.domain.reader.chapter_view import ChapterView
from SanskritAI.domain.reader.sloka_view import SlokaView
from SanskritAI.domain.reader.word_view import WordView
@dataclass(slots=True)
class ReaderController:
    """Application-facing controller for an active ReaderSession."""
    session: ReaderSession
    @classmethod
    def open(cls, engine: ReaderEngine, position: ReaderPosition) -> "ReaderController":
        """Create a controller with a newly opened ReaderSession."""
        return cls(session=ReaderSession.open(engine, position))
    @property
    def engine(self) -> ReaderEngine:
        """Return the ReaderEngine owned by the active session."""
        return self.session.engine
    @property
    def position(self) -> ReaderPosition | None:
        """Return the current ReaderPosition."""
        return self.session.current_position
    @property
    def current_position(self) -> ReaderPosition | None:
        """Return the current ReaderPosition."""
        return self.session.current_position
    @property
    def has_position(self) -> bool:
        """Return True when the controller has a current position."""
        return self.session.has_position
    @property
    def result(self) -> Any:
        """Return the current ReaderResult, if available."""
        return self.session.current_result
    @property
    def current_result(self) -> Any:
        """Return the current ReaderResult, if available."""
        return self.session.current_result
    @property
    def has_result(self) -> bool:
        """Return True when a ReaderResult is available."""
        return self.session.has_result
    @property
    def succeeded(self) -> bool:
        """Return the success state of the current ReaderResult."""
        return self.session.succeeded
    @property
    def can_go_back(self) -> bool:
        """Return whether browser-style back navigation is available."""
        return self.session.can_go_back
    @property
    def can_go_forward(self) -> bool:
        """Return whether browser-style forward navigation is available."""
        return self.session.can_go_forward
    @property
    def history_count(self) -> int:
        """Return the controller-visible navigation history count."""
        count = self.session.history_count
        if count == 0 and self.session.has_position:
            return 1
        return count
    def open_position(self, position: ReaderPosition) -> ReaderPosition | None:
        """Open a new mutable browsing root at position."""
        return self.session.set_position(position)
    def set_position(self, position: ReaderPosition | None) -> ReaderPosition | None:
        """Set a new browsing root through ReaderSession."""
        return self.session.set_position(position)
    def resolve(self) -> ReaderSession:
        """Return a re-resolved immutable session."""
        return self.session.resolve()
    def next(self) -> ReaderPosition | None:
        """Perform stateful forward structural navigation."""
        return self.session.next()
    def previous(self) -> ReaderPosition | None:
        """Perform stateful backward structural navigation."""
        return self.session.previous()
    def back(self) -> ReaderPosition | None:
        """Perform browser-style history back navigation."""
        return self.session.back()
    def forward(self) -> ReaderPosition | None:
        """Perform browser-style history forward navigation."""
        return self.session.forward()
    def move_next(self) -> ReaderSession | None:
        """Return a new session at the next structural position."""
        return self.session.move_next()
    def move_previous(self) -> ReaderSession | None:
        """Return a new session at the previous structural position."""
        return self.session.move_previous()
    def clear_history(self) -> None:
        """Clear session history while preserving the current position."""
        self.session.clear_history()
    def document(self, document_id: str | None = None) -> ReaderDocument:
        """Resolve a ReaderDocument through ReaderEngine."""
        return self.engine.document(document_id)
    def chapter(self, chapter_id: str) -> ChapterView:
        """Resolve a ChapterView through ReaderEngine."""
        return self.engine.chapter(chapter_id)
    def sloka(self, sloka_id: str) -> SlokaView:
        """Resolve a SlokaView through ReaderEngine."""
        return self.engine.sloka(sloka_id)
    def word(self, word_id: str) -> WordView:
        """Resolve a WordView through ReaderEngine."""
        return self.engine.word(word_id)
    def resolve_position(self, position: ReaderPosition) -> ChapterView | SlokaView | WordView:
        """Resolve an arbitrary ReaderPosition through ReaderEngine."""
        return self.engine.resolve(position)
    @property
    def display_name(self) -> str:
        """Return the controller display name."""
        return "Reader Controller"
    @property
    def display_text(self) -> str:
        """Return the current session display text."""
        return self.session.display_text
    @property
    def display_description(self) -> str:
        """Return the controller display description."""
        return "Application-facing controller for the active Reader session."
    def __str__(self) -> str:
        return self.display_text
