"""
SanskritAI
==========

Module:
    services.importers.parser_context

Description
-----------
Active parser execution context for corpus importers.

ParserContext manages:
    • parser state
    • current input line
    • Amarakośa hierarchy ownership
    • import statistics
    • structured parser diagnostics

Version
-------
v0.5.0-alpha
"""

from __future__ import annotations

try:
    from SanskritAI.models.amarakosha import (
        Amarakosha,
        Kanda,
        Varga,
        Verse,
    )
    from SanskritAI.models.imports import (
        ImportError,
        ImportStatistics,
    )
except ImportError:
    from models.amarakosha import (
        Amarakosha,
        Kanda,
        Varga,
        Verse,
    )
    from models.imports import (
        ImportError,
        ImportStatistics,
    )

from .parser_state import ParserState
from .parser_errors import StructureError


class ParserContext:
    """
    Active execution context for the parsing lifecycle.

    Responsibilities
    ----------------
    • Maintain parser FSM state.
    • Track current source line.
    • Own the active Amarakośa hierarchy during parsing.
    • Collect import statistics.
    • Collect structured parser diagnostics.
    """

    def __init__(self, edition_id: str = "default") -> None:
        self.state: ParserState = ParserState.START
        self.line_number: int = 0
        self.current_line: str = ""

        # Domain hierarchy
        self.book: Amarakosha = Amarakosha(edition_id=edition_id)
        self._current_kanda: Kanda | None = None
        self._current_varga: Varga | None = None
        self._current_verse: Verse | None = None

        # Import execution metrics & diagnostics
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
        """Advance the parser to the next source line."""
        self.line_number += 1
        self.current_line = line

    def transition(self, next_state: ParserState) -> None:
        """Validate and perform a parser-state transition."""
        if not self.state.can_transition_to(next_state):
            raise StructureError(
                f"Illegal state transition from {self.state.name} to {next_state.name}.",
                self.line_number,
            )
        self.state = next_state

    def enter_kanda(self, kanda: Kanda) -> None:
        """Enter and register a Kāṇḍa."""
        self.book.add_kanda(kanda)
        self._current_kanda = kanda
        self._current_varga = None
        self._current_verse = None
        self.statistics.kandas = len(self.book.kandas)

    def enter_varga(self, varga: Varga) -> None:
        """Enter and register a Varga inside the active Kāṇḍa."""
        if self._current_kanda is None:
            raise StructureError(
                "Cannot enter a Varga without an active Kāṇḍa context.",
                self.line_number,
            )
        self._current_kanda.add_varga(varga)
        self._current_varga = varga
        self._current_verse = None
        self.statistics.vargas += 1

    def enter_verse(self, verse: Verse) -> None:
        """Enter and register a Verse inside the active Varga."""
        if self._current_varga is None:
            raise StructureError(
                "Cannot enter a Verse without an active Varga context.",
                self.line_number,
            )
        self._current_varga.add_verse(verse)
        self._current_verse = verse
        self.statistics.verses += 1

    def add_error(
        self,
        message: str,
        severity: str = "warning",
    ) -> None:
        """
        Add a structured parser diagnostic.

        Fatal or error diagnostics increment error counters.
        Warnings increment warning counters.
        """
        error = ImportError(
            line_number=self.line_number,
            message=message,
            severity=severity,
        )
        self.errors.append(error)

        if severity.lower() in {"fatal", "error"}:
            self.statistics.errors += 1
        else:
            self.statistics.warnings += 1
