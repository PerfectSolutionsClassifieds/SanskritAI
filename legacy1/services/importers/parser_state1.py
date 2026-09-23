"""
SanskritAI
==========

Module:
    services.importers.parser_state

Description
-----------
Finite-state machine definitions for corpus parsers.

A parser progresses through a sequence of well-defined states
while constructing a canonical domain model.

The same state machine concept is reusable across all SanskritAI
text importers.

Examples
--------
    Amarakośa

    Śiva Purāṇa

    Devī Bhāgavata

    Mahābhārata

    Rāmāyaṇa

Version:
    v0.4.0
"""

from __future__ import annotations

from enum import Enum


class ParserState(Enum):
    """
    Parser state machine.

    Typical workflow
    ----------------

        START

            ↓

        EXPECT_KANDA

            ↓

        EXPECT_VARGA

            ↓

        EXPECT_VERSE

            ↓

        EXPECT_VERSE

            ↓

        EXPECT_VARGA

            ↓

        ...

            ↓

        FINISHED
    """

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    START = "Start"

    FINISHED = "Finished"

    ERROR = "Error"

    # ---------------------------------------------------------
    # Structural Expectations
    # ---------------------------------------------------------

    EXPECT_KANDA = "Expect Kanda"

    EXPECT_VARGA = "Expect Varga"

    EXPECT_VERSE = "Expect Verse"

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_terminal(self) -> bool:
        """
        True if parsing has reached a terminal state.
        """

        return self in {
            ParserState.FINISHED,
            ParserState.ERROR,
        }

    @property
    def expects_structure(self) -> bool:
        """
        True when parser expects a structural element.
        """

        return self in {
            ParserState.EXPECT_KANDA,
            ParserState.EXPECT_VARGA,
            ParserState.EXPECT_VERSE,
        }

    @property
    def is_running(self) -> bool:
        """
        True while actively parsing.
        """

        return (
            not self.is_terminal
            and self is not ParserState.START
        )

    # ---------------------------------------------------------
    # State Transitions
    # ---------------------------------------------------------

    def can_transition_to(
        self,
        next_state: "ParserState",
    ) -> bool:
        """
        Validate a state transition.

        This provides lightweight finite-state validation.
        """

        transitions = {

            ParserState.START: {
                ParserState.EXPECT_KANDA,
                ParserState.ERROR,
            },

            ParserState.EXPECT_KANDA: {
                ParserState.EXPECT_VARGA,
                ParserState.ERROR,
                ParserState.FINISHED,
            },

            ParserState.EXPECT_VARGA: {
                ParserState.EXPECT_VERSE,
                ParserState.EXPECT_KANDA,
                ParserState.ERROR,
                ParserState.FINISHED,
            },

            ParserState.EXPECT_VERSE: {
                ParserState.EXPECT_VERSE,
                ParserState.EXPECT_VARGA,
                ParserState.EXPECT_KANDA,
                ParserState.ERROR,
                ParserState.FINISHED,
            },

            ParserState.FINISHED: set(),

            ParserState.ERROR: set(),
        }

        return next_state in transitions[self]

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:

        return self.value

    def __repr__(self) -> str:

        return f"ParserState.{self.name}"
