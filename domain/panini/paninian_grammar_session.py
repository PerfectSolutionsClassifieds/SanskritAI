from __future__ import annotations

"""
SanskritAI
==========

Paninian Grammar Session

Runtime execution session for one Paninian
grammatical derivation.

Purpose
-------

PaninianGrammar remains immutable.

PaninianGrammarSession stores all mutable runtime
state produced during one derivation.

Architecture
------------

PaninianGrammar
        │
creates ▼
PaninianGrammarSession
        │
        ├── current_context
        ├── execution_trace
        ├── derivation_engine
        ├── statistics
        └── diagnostics

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)

from SanskritAI.domain.panini.paninian_derivation_engine import (
    PaninianDerivationEngine,
)

from SanskritAI.domain.panini.paninian_execution_trace import (
    PaninianExecutionTrace,
)

from SanskritAI.domain.panini.paninian_grammar import (
    PaninianGrammar,
)


@dataclass(slots=True)
class PaninianGrammarSession:
    """
    Runtime execution session.
    """

    grammar: PaninianGrammar

    context: PaninianDerivationContext

    engine: PaninianDerivationEngine = field(
        default_factory=PaninianDerivationEngine,
    )

    trace: PaninianExecutionTrace = field(
        default_factory=PaninianExecutionTrace,
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    completed: bool = False

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def run(
        self,
    ) -> PaninianDerivationContext:
        """
        Executes one derivation session.
        """

        self.engine.clear_trace()

        self.context = self.engine.derive(
            self.context,
        )

        self.trace = self.engine.execution_trace

        self.completed = True

        return self.context

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def executed_rule_count(
        self,
    ) -> int:

        return self.trace.step_count

    @property
    def current_iteration(
        self,
    ) -> int:

        return self.context.iteration

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "completed":
                self.completed,

            "iteration":
                self.current_iteration,

            "executed_rules":
                self.executed_rule_count,

            "grammar":
                str(self.grammar),

            "engine":
                self.engine.summary(),

        }

    # ---------------------------------------------------------
    # Session management
    # ---------------------------------------------------------

    def reset(
        self,
        context: PaninianDerivationContext,
    ) -> None:
        """
        Starts a fresh derivation session.
        """

        self.context = context

        self.completed = False

        self.engine.clear_trace()

        self.trace = PaninianExecutionTrace()

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return (
            "PaninianGrammarSession("
            f"{self.executed_rule_count} executed rules)"
        )
