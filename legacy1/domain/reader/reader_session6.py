from __future__ import annotations
"""
SanskritAI
==========
Reader Session
Stateful reader-session façade built on top of ReaderEngine and ReaderSessionHistory.
ReaderEngine owns structural corpus navigation.
ReaderSessionHistory owns browser-style history.
ReaderSession provides the user-facing session state.
The API intentionally supports two navigation styles:
    next()/previous()
        Stateful navigation. The existing session is updated.
    move_next()/move_previous()
        Immutable navigation. A new ReaderSession is returned.
This allows the session domain tests and the higher-level integration tests to
share the same ReaderSession abstraction without weakening either contract.
"""
from dataclasses import dataclass, field
from typing import Any
from SanskritAI.domain.reader.reader_engine import ReaderEngine
from SanskritAI.domain.reader.reader_position import ReaderPosition
from SanskritAI.domain.reader.reader_session_history import ReaderSessionHistory

@dataclass(slots=True)
class ReaderSession:
    engine: ReaderEngine
    history: ReaderSessionHistory = field(default_factory=ReaderSessionHistory)
    position: ReaderPosition | None = None
    _result: Any = field(default=None, repr=False)
    @property
    def current_position(self) -> ReaderPosition | None:
        return self.position
    @property
    def has_position(self) -> bool:
        return self.position is not None
    @property
    def result(self) -> Any:
        return self._result
    @property
    def current_result(self) -> Any:
        return self._result
    @property
    def has_result(self) -> bool:
        return self._result is not None
    @property
    def succeeded(self) -> bool:
        if self._result is None:
            return False
        return bool(getattr(self._result, "succeeded", False))
    @property
    def can_go_back(self) -> bool:
        return self.history.can_go_back
    @property
    def can_go_forward(self) -> bool:
        return self.history.can_go_forward
    @property
    def history_count(self) -> int:
        return self.history.count
    def open(
        self=None,
        position: ReaderPosition | None = None,
        *,
        engine: ReaderEngine | None = None,
    ):
        """
        Open a ReaderSession.
        Supported forms:
            ReaderSession.open(engine, position)
            ReaderSession.open(engine=engine, position=position)
            session.open(position)
        Class-style calls create a new immutable session rooted at position.
        Instance-style calls establish a new mutable browsing root.
        """
        if isinstance(self, ReaderSession):
            if engine is not None:
                raise TypeError("engine cannot be supplied when opening an existing ReaderSession.")
            if position is None:
                raise ValueError("position must not be None when opening an existing ReaderSession.")
            return self.set_position(position)
        if engine is None:
            engine = self
        if not isinstance(engine, ReaderEngine):
            raise TypeError("ReaderSession.open() requires a ReaderEngine.")
        if position is None:
            raise ValueError("ReaderSession.open() requires a ReaderPosition.")
        result = engine.resolve(position)
        return ReaderSession(
            engine=engine,
            position=position,
            _result=result,
        )
    def set_position(self, position: ReaderPosition | None) -> ReaderPosition | None:
        """
        Establish a new mutable browsing root.
        Existing history is discarded.
        The supplied position becomes the initial history entry.
        """
        self.position = position
        self._result = None
        self.history.clear()
        if position is not None:
            self.history.record(position)
        return self.position
    def resolve(self) -> ReaderSession:
        """
        Re-resolve the current position without mutating this session.
        """
        if self.position is None:
            return ReaderSession(
                engine=self.engine,
                history=self._copy_history(),
                position=None,
                _result=None,
            )
        result = self.engine.resolve(self.position)
        return ReaderSession(
            engine=self.engine,
            history=self._copy_history(),
            position=self.position,
            _result=result,
        )
    def next(self) -> ReaderPosition | None:
        """
        Stateful structural navigation.
        Successful navigation updates this session and records the new
        position in session history.
        """
        if self.position is None:
            return None
        result = self.engine.move_next(self.position)
        if result is None:
            return None
        self.position = result
        self._result = None
        self.history.record(result)
        return result
    def previous(self) -> ReaderPosition | None:
        """
        Stateful structural navigation in the previous direction.
        Successful navigation updates this session and records the new
        position in session history.
        """
        if self.position is None:
            return None
        result = self.engine.move_previous(self.position)
        if result is None:
            return None
        self.position = result
        self._result = None
        self.history.record(result)
        return result
    def move_next(self) -> ReaderSession | None:
        """
        Immutable structural navigation.
        The original session remains unchanged.
        """
        if self.position is None:
            return None
        result = self.engine.move_next(self.position)
        if result is None:
            return None
        return ReaderSession.open(
            self.engine,
            result,
        )
    def move_previous(self) -> ReaderSession | None:
        """
        Immutable structural navigation in the previous direction.
        The original session remains unchanged.
        """
        if self.position is None:
            return None
        result = self.engine.move_previous(self.position)
        if result is None:
            return None
        return ReaderSession.open(
            self.engine,
            result,
        )
    def back(self) -> ReaderPosition | None:
        """
        Stateful browser-history backward navigation.
        ReaderEngine is not invoked.
        """
        result = self.history.back()
        if result is None:
            return None
        self.position = result
        self._result = None
        return result
    def forward(self) -> ReaderPosition | None:
        """
        Stateful browser-history forward navigation.
        ReaderEngine is not invoked.
        """
        result = self.history.forward()
        if result is None:
            return None
        self.position = result
        self._result = None
        return result
    def clear_history(self) -> None:
        """
        Clear session history without clearing the current position.
        """
        self.history.clear()
    def _copy_history(self) -> ReaderSessionHistory:
        """
        Create an independent copy of the current history state.
        Uses the public ReaderSessionHistory API rather than depending on
        its private stack representation.
        """
        copied = ReaderSessionHistory()
        entries: list[ReaderPosition] = []
        current = self.history.current
        back_entries: list[ReaderPosition] = []
        cursor = current
        while cursor is not None and self.history.can_go_back:
            previous = self.history.previous
            if previous is None:
                break
            back_entries.append(previous)
            break
        if current is not None:
            copied.record(current)
        return copied
    @property
    def display_name(self) -> str:
        return "Reader Session"
    @property
    def display_text(self) -> str:
        if self._result is not None and hasattr(self._result, "display_text"):
            return self._result.display_text
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
