"""
SanskritAI
==========

Module:
    services.importers.parser_context

Description
-----------
Maintains the mutable state of a parser during corpus import.

The ParserContext tracks:

    • Current parser state
    • Current line number
    • Current structural objects
    • Import statistics
    • Import diagnostics

ParserContext intentionally contains no parsing logic.
It serves as shared state for the parser state machine.

Version:
    v0.4.0
"""

from __future__ import annotations

from dataclasses import dataclass, field

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


@dataclass(slots=True)
class ParserContext:
    """
    Mutable parser state.

    One ParserContext instance exists for the lifetime of a
    single parser execution.
    """

    # ---------------------------------------------------------
    # Parser State
    # ---------------------------------------------------------

    state: ParserState = ParserState.START

    line_number: int = 0

    # ---------------------------------------------------------
    # Domain Objects
    # ---------------------------------------------------------

    book: Amarakosha = field(
        default_factory=Amarakosha
    )

    current_kanda: Kanda | None = None

    current_varga: Varga | None = None

    current_verse: Verse | None = None

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    statistics: ImportStatistics = field(
        default_factory=ImportStatistics
    )

    errors: list[ImportError] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Line Tracking
    # ---------------------------------------------------------

    current_line: str = ""

    # ---------------------------------------------------------
    # State Management
    # ---------------------------------------------------------

    def transition(
        self,
        new_state: ParserState,
    ) -> None:
        """
        Transition to another parser state.

        Raises
        ------
        ValueError
            If the transition is invalid.
        """

        if not self.state.can_transition_to(new_state):

            raise ValueError(

                f"Illegal parser transition "

                f"{self.state.name} -> {new_state.name}"

            )

        self.state = new_state

    # ---------------------------------------------------------
    # Line Management
    # ---------------------------------------------------------

    def next_line(
        self,
        line: str,
    ) -> None:
        """
        Advance parser to the next input line.
        """

        self.line_number += 1

        self.current_line = line

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def add_error(
        self,
        error: ImportError,
    ) -> None:
        """
        Register one parsing error.
        """

        self.errors.append(error)

        if error.is_warning:

            self.statistics.warnings += 1

        elif error.is_error:

            self.statistics.errors += 1

        elif error.is_fatal:

            self.statistics.errors += 1

            self.state = ParserState.ERROR

    # ---------------------------------------------------------
    # Statistics Helpers
    # ---------------------------------------------------------

    def increment_kanda(self) -> None:

        self.statistics.books = 1

        self.statistics.sections += 1

    def increment_varga(self) -> None:

        self.statistics.groups += 1

    def increment_verse(self) -> None:

        self.statistics.records += 1

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def has_errors(self) -> bool:

        return self.statistics.errors > 0

    @property
    def has_warnings(self) -> bool:

        return self.statistics.warnings > 0

    @property
    def current_location(self) -> str:
        """
        Human-readable parser location.
        """

        parts = []

        if self.current_kanda is not None:
            parts.append(
                f"Kāṇḍa {self.current_kanda.number}"
            )

        if self.current_varga is not None:
            parts.append(
                f"Varga {self.current_varga.number}"
            )

        if self.current_verse is not None:
            parts.append(
                f"Verse {self.current_verse.number}"
            )

        if not parts:
            return "Beginning of document"

        return " → ".join(parts)

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset parser context for reuse.
        """

        self.state = ParserState.START

        self.line_number = 0

        self.current_line = ""

        self.book = Amarakosha()

        self.current_kanda = None

        self.current_varga = None

        self.current_verse = None

        self.statistics = ImportStatistics()

        self.errors.clear()

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (

            "ParserContext("

            f"state={self.state.name}, "

            f"line={self.line_number}, "

            f"errors={self.statistics.errors}, "

            f"warnings={self.statistics.warnings})"

        )
