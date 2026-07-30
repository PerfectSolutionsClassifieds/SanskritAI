from __future__ import annotations

"""
SanskritAI
==========

Gana Match Rule

Concrete heuristic rule that resolves Dhatu candidates by gana
metadata.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.dhatu.dhatu_context import DhatuContext
from SanskritAI.domain.dhatu.dhatu_gana import BVADI, DhatuGana
from SanskritAI.domain.dhatu.dhatu_rule import DhatuRule


class GanaMatchRule(
    DhatuRule,
):
    """
    Heuristic rule for gana-based dhatu matching.
    """

    _GANAS: tuple[DhatuGana, ...] = (
        BVADI,
    )

    @property
    def display_name(self) -> str:
        return "Gana Match Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic rule for gana-based dhatu matching."

    def _extract_text(self, context: DhatuContext) -> str:
        return str(context.subject).strip()

    def applies_to(self, context: DhatuContext) -> bool:
        text = self._extract_text(context)
        if not text:
            return False

        gana_hint = str(context.get("gana", "")).lower()
        return bool(gana_hint) or context.has_metadata

    def apply(self, context: DhatuContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = self._extract_text(context)
        gana_hint = str(context.get("gana", "")).lower()

        outputs: list[Dhatu] = []

        for index, gana in enumerate(self._GANAS, start=1):
            if not gana_hint or gana_hint in {gana.identifier, gana.sanskrit_name.lower(), gana.english_name.lower()}:
                outputs.append(
                    Dhatu(
                        identifier=f"{context.identifier}:gana:{index}",
                        root=text,
                        transliteration=context.get("transliteration", ""),
                        meaning=str(context.get("meaning", "")),
                        gana=gana,
                    )
                )

        return tuple(outputs)
