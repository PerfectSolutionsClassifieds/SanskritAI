"""
SanskritAI
==========

Module:
    services.importers.parser_validator

Description
-----------
Pure validation engine assessing state transitions, operational hierarchy,
and post-parse structure completeness.

Version
-------
v0.5.0-alpha
"""

from __future__ import annotations

try:
    from SanskritAI.models.amarakosha import Amarakosha
except ImportError:
    from models.amarakosha import Amarakosha

from .parser_state import ParserState
from .parser_errors import StructureError, ValidationError


class ParserValidator:
    """
    Validates structural states and completeness constraints
    across the active parser lifecycle.
    """

    @staticmethod
    def validate_transition(
        current_state: ParserState,
        next_state: ParserState,
        line_number: int,
    ) -> None:
        """Verifies if the finite state machine can transition safely."""
        if not current_state.can_transition_to(next_state):
            raise StructureError(
                f"Illegal state machine transition: '{current_state.name}' -> '{next_state.name}'.",
                line_number,
            )

    @staticmethod
    def validate_hierarchy_presence(
        active_parent: object | None,
        entity_type: str,
        line_number: int,
    ) -> None:
        """Ensures structural nested context criteria are met before attaching children."""
        if active_parent is None:
            raise StructureError(
                f"Structural anomaly: Found {entity_type} without an active parent scope context.",
                line_number,
            )

    @staticmethod
    def validate_completion(book: Amarakosha) -> list[str]:
        """
        Deep structural integrity check on completion.
        Returns a list of warning descriptions for non-fatal structural gaps.
        """
        warnings: list[str] = []

        if not book.kandas:
            raise ValidationError(
                "Imported Amarakośa volume contains zero structural Kāṇḍas.",
                line_number=0,
            )

        for kanda in book.kandas:
            k_title = getattr(kanda, "title", str(kanda))
            if not getattr(kanda, "vargas", []):
                warnings.append(f"Kāṇḍa '{k_title}' contains zero structural Vargas.")

            for varga in getattr(kanda, "vargas", []):
                v_title = getattr(varga, "title", str(varga))
                if not getattr(varga, "verses", []):
                    warnings.append(f"Varga '{v_title}' contains zero structural Verses.")

        return warnings
