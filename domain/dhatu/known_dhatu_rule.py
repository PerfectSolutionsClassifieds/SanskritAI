from __future__ import annotations

"""
SanskritAI
==========

Known Dhatu Rule

Concrete heuristic rule that resolves known धातु roots from
metadata or a small canonical lookup table.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.dhatu.dhatu_context import DhatuContext
from SanskritAI.domain.dhatu.dhatu_rule import DhatuRule


class KnownDhatuRule(
    DhatuRule,
):
    """
    Heuristic rule for known dhatu matching.
    """

    _BOOTSTRAP_ROOTS: tuple[tuple[str, str, str], ...] = (
        ("भू", "bhū", "to be"),
        ("गम्", "gam", "to go"),
        ("पठ्", "paṭh", "to read"),
        ("कृ", "kṛ", "to do"),
        ("दृश्", "dṛś", "to see"),
        ("नी", "nī", "to lead"),
        ("स्था", "sthā", "to stand"),
    )

    @property
    def display_name(self) -> str:
        return "Known Dhatu Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic rule for known dhatu roots."

    def _extract_text(self, context: DhatuContext) -> str:
        return str(context.subject).strip()

    def _hinted(self, context: DhatuContext) -> bool:
        hint = str(context.get("dhatu_hint", "")).lower()
        return hint in {"known", "root", "dhatu", "dhātu"}

    def applies_to(self, context: DhatuContext) -> bool:
        text = self._extract_text(context)
        if not text:
            return False

        if self._hinted(context):
            return True

        return any(text == root or text == transliteration for root, transliteration, _ in self._BOOTSTRAP_ROOTS)

    def apply(self, context: DhatuContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = self._extract_text(context)
        outputs: list[Dhatu] = []

        for index, (root, transliteration, meaning) in enumerate(self._BOOTSTRAP_ROOTS, start=1):
            if text == root or text == transliteration or self._hinted(context):
                outputs.append(
                    Dhatu(
                        identifier=f"{context.identifier}:dhatu:{index}",
                        root=root,
                        transliteration=transliteration,
                        meaning=meaning,
                    )
                )

        return tuple(outputs)
