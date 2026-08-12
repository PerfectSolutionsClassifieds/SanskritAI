from __future__ import annotations
from dataclasses import dataclass, field
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_session_history import ReaderSessionHistory
@dataclass(slots=True)
class ReaderSession:
    """
    Stateful reader session coordinating structural ReaderEngine navigation
    and browser-style ReaderSessionHistory navigation.
    """
    engine: ReaderEngine
    history: ReaderSessionHistory = field(default_factory=ReaderSessionHistory)
    position: ReaderPosition | None = None
    _implicit_initial_position: ReaderPosition | None = field(default=None, init=False, repr=False)
    def __post_init__(self) -> None:
        """
        A constructor-supplied position is the current session position but
        is not initially counted as a history entry.
        """
        if self.position is not None and self.history.is_empty:
            self._implicit_initial_position = self.position
    @property
    def current_position(self) -> ReaderPosition | None:
        return self.position
    @property
    def has_position(self) -> bool:
        return self.position is not None
    @property
    def can_go_back(self) -> bool:
        if self.position is None:
            return False
        if self._implicit_initial_position is not None and self.history.is_empty:
            return False
        if self._implicit_initial_position is not None and self.history.current is not self.position:
            return True
        return self.history.can_go_back
    @property
    def can_go_forward(self) -> bool:
        return self.history.can_go_forward
    @property
    def history_count(self) -> int:
        """
        Explicitly opened sessions expose the complete history count.
        Constructor-initialized sessions exclude their implicit root.
        """
        count = self.history.history_count
        if self._implicit_initial_position is not None and count > 0:
            return max(0, count - 1)
        return count
    def open(self, position: ReaderPosition) -> ReaderPosition:
        """
        Establish an explicit browsing root.
        Unlike constructor initialization, open() records the root as history.
        """
        result = self.set_position(position)
        assert result is not None
        return result
    def set_position(self, position: ReaderPosition | None) -> ReaderPosition | None:
        """
        Establish a new explicit position and replace the existing history.
        """
        self.position = position
        self.history.clear()
        self._implicit_initial_position = None
        if position is not None:
            self.history.record(position)
        return self.position
    def _ensure_implicit_root_in_history(self) -> None:
        """
        Ensure a constructor-supplied root exists in history before a
        structural or browser-style navigation needs it.
        """
        if self._implicit_initial_position is None:
            return
        root = self._implicit_initial_position
        current = self.history.current
        if current is None:
            self.history.record(root)
        elif current is not root:
            self.history.clear()
            self.history.record(root)
        self._implicit_initial_position = root
    def _prepare_structural_navigation(self) -> None:
        """
        Preserve the constructor-supplied root while allowing the structural
        result to become a subsequent history entry.
        """
        if self._implicit_initial_position is not None and self.history.is_empty:
            self.history.record(self._implicit_initial_position)
    def next(self) -> ReaderPosition | None:
        """
        Navigate forward structurally through ReaderEngine.
        Successful structural moves are recorded in session history.
        """
        if self.position is None:
            return None
        result = self.engine.move_next(self.position)
        if result is None:
            return None
        self._prepare_structural_navigation()
        self.position = result
        self.history.record(result)
        return result
    def previous(self) -> ReaderPosition | None:
        """
        Navigate backward structurally through ReaderEngine.
        Successful structural moves are recorded in session history.
        """
        if self.position is None:
            return None
        result = self.engine.move_previous(self.position)
        if result is None:
            return None
        self._prepare_structural_navigation()
        self.position = result
        self.history.record(result)
        return result
    def back(self) -> ReaderPosition | None:
        """
        Navigate backward through browser-style session history.
        A constructor-supplied root is inserted when necessary so manually
        recorded history can still branch from the current session position.
        """
        if self.position is None:
            return None
        if self._implicit_initial_position is not None:
            if self.history.is_empty:
                return None
            if self.history.current is not self.position:
                root = self._implicit_initial_position
                self.history.clear()
                self.history.record(root)
                self.history.record(self.position)
        result = self.history.back()
        if result is None:
            return None
        self.position = result
        return result
    def forward(self) -> ReaderPosition | None:
        """
        Navigate forward through browser-style session history.
        """
        result = self.history.forward()
        if result is None:
            return None
        self.position = result
        return result
    def clear_history(self) -> None:
        """
        Clear browser-style history without clearing the current position.
        """
        self.history.clear()
        self._implicit_initial_position = None
    @property
    def display_name(self) -> str:
        return "Reader Session"
    @property
    def display_text(self) -> str:
        if self.position is None:
            return "Reader Session"
        return str(self.position)
    @property
    def display_description(self) -> str:
        if self.position is None:
            return "Reader session without a current position."
        return "Stateful Reader session with navigation history."
    def __str__(self) -> str:
        return self.display_text
