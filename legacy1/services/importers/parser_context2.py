
"""
SanskritAI
==========

Module:
    services.importers.parser_context_v2

Description
-----------
Active Domain Context manager that handles state transitions, 
tracks deep hierarchy ownership safely, and automates event-driven statistics.

Version
-------
v0.5.0-alpha
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from models.amarakosha import Amarakosha, Kanda, Varga, Verse
from models.imports import ImportError, ImportStatistics
from services.importers.parser_state import ParserState
from services.importers.parser_errors import StructureError

# ParserContextV2
class ParserContext:
    """
    Active execution context for the parsing lifecycle.
    Encapsulates state validation, statistics updates, and object tracking.
    """

    def __init__(self) -> None:
        self.state: ParserState = ParserState.START
        self.line_number: int = 0
        self.current_line: str = ""
        
        self.book: Amarakosha = Amarakosha()
        self._current_kanda: Kanda | None = None
        self._current_varga: Varga | None = None
        self._current_verse: Verse | None = None

        self.statistics: ImportStatistics = ImportStatistics()
        self.errors: list[ImportError] = []

    @property
    def current_kanda(self) -> Kanda | None:
        return self._current_kanda

    @property
    def current_varga(self) -> Varga | None:
        return self._current_varga

    @property
    def current_verse(self) -> Verse | None:
        return self._current_verse

    def next_line(self, line: str) -> None:
        self.line_number += 1
        self.current_line = line

    def transition(self, next_state: ParserState) -> None:
        """Enforces robust FSM transition constraints."""
        if not self.state.can_transition_to(next_state):
            raise StructureError(
                f"Illegal state transition from {self.state.name} to {next_state.name}.",
                self.line_number
            )
        self.state = next_state

    # -------------------------------------------------------------------------
    # Active Domain Tracking (Event-Driven Statistics & State Containment)
    # -------------------------------------------------------------------------

    def enter_kanda(self, kanda: Kanda) -> None:
        """Registers a Kanda, tracking its lifecycle safely."""
        self.book.add_kanda(kanda)
        self._current_kanda = kanda
        self._current_varga = None
        self._current_verse = None
        
        # Event-driven statistics calculation
        self.statistics.kandas = len(self.book.kandas)

    def enter_varga(self, varga: Varga) -> None:
        """Registers a Varga inside the active Kanda context."""
        if self._current_kanda is None:
            raise StructureError("Cannot enter a Varga without an active Kāṇḍa context.", self.line_number)
        
        self._current_kanda.add_varga(varga)
        self._current_varga = varga
        self._current_verse = None
        
        # Event-driven tracking update
        self.statistics.vargas += 1

    def enter_verse(self, verse: Verse) -> None:
        """Registers a Verse inside the active Varga context."""
        if self._current_varga is None:
            raise StructureError("Cannot enter a Verse without an active Varga context.", self.line_number)
        
        self._current_varga.add_verse(verse)
        self._current_verse = verse
        
        # Event-driven tracking update
        self.statistics.verses += 1

    def add_error(self, message: str, severity: str = "warning") -> None:
        """Appends error diagnostics and increments internal stats counters."""
        err = ImportError(
            line_number=self.line_number,
            message=message,
            severity=severity
        )
        self.errors.append(err)
        if severity == "fatal":
            self.statistics.errors += 1
        else:
            self.statistics.warnings += 1
