from __future__ import annotations

"""
SanskritAI
==========

Jihvamuliya Rule

Realizes Visarga as Jihvāmūlīya before
क / ख.

Hierarchy
---------

VisargaSandhiRule
        │
        ▼
VisargaAllophoneRule
        │
        ▼
JihvamuliyaRule
"""

from SanskritAI.domain.sandhi.sandhi_context import SandhiContext
from SanskritAI.domain.sandhi.visarga_allophone_rule import (
    VisargaAllophoneRule,
)


class JihvamuliyaRule(
    VisargaAllophoneRule,
):

    _FOLLOWING = (
        "क",
        "ख",
    )

    @property
    def display_name(self):
        return "Jihvamuliya Rule"

    @property
    def display_description(self):
        return (
            "Realizes Visarga as Jihvāmūlīya."
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
            left[:-1] + "ᳵ" + right,
        )
