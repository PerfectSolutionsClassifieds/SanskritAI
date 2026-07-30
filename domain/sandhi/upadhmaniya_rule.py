from __future__ import annotations

"""
SanskritAI
==========

Upadhmaniya Rule

Realizes Visarga as Upadhmānīya before
प / फ.

Hierarchy
---------

VisargaSandhiRule
        │
        ▼
VisargaAllophoneRule
        │
        ▼
UpadhmaniyaRule
"""

from SanskritAI.domain.sandhi.sandhi_context import SandhiContext
from SanskritAI.domain.sandhi.visarga_allophone_rule import (
    VisargaAllophoneRule,
)


class UpadhmaniyaRule(
    VisargaAllophoneRule,
):

    _FOLLOWING = (
        "प",
        "फ",
    )

    @property
    def display_name(self):
        return "Upadhmaniya Rule"

    @property
    def display_description(self):
        return (
            "Realizes Visarga as Upadhmānīya."
        )

    def _extract_words(self, context):

        parts = str(context.subject).split()

        if len(parts) != 2:
            return None

        return parts[0], parts[1]

    def applies_to(self, context):

        words = self._extract_words(context)

        if words is None:
            return False

        left, right = words

        return (
            left.endswith("ः")
            and right.startswith(self._FOLLOWING)
        )

    def apply(self, context):

        words = self._extract_words(context)

        if words is None:
            return tuple()

        left, right = words

        return (
            left[:-1] + "ᳶ" + right,
        )
