from __future__ import annotations

"""
SanskritAI
==========

Upstream Vakya Rules

Provides sentence-analysis rules that enrich Vakya outputs
from upstream kernel metadata such as Derivation, Samasa,
Sandhi, and Grammar.

These rules let the sentence layer behave more like a real
aggregator of linguistic structure rather than only a generic
metadata wrapper.

Version
-------
v1.1.0
"""

from typing import Any

from SanskritAI.domain.vakya.vakya_context import VakyaContext
from SanskritAI.domain.vakya.vakya_rule import VakyaRule


class _MetadataUpstreamVakyaRule(
    VakyaRule,
):
    """
    Helper base class for metadata-driven sentence rules.
    """

    metadata_key: str = ""
    analysis_type: str = ""
    summary_label: str = ""
    structural_role: str = ""

    def _describe(self, value: Any) -> str:
        if hasattr(value, "display_text"):
            return str(getattr(value, "display_text"))
        return str(value)

    def _to_components(self, value: Any) -> tuple[Any, ...]:
        if value is None:
            return tuple()
        if isinstance(value, tuple):
            return value
        if isinstance(value, list):
            return tuple(value)
        return (value,)

    def applies_to(self, context: VakyaContext) -> bool:
        return context.get(self.metadata_key, None) is not None

    def apply(self, context: VakyaContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        value = context.get(self.metadata_key)
        sentence = str(context.subject).strip()

        analysis_label = self.summary_label or self.metadata_key.title()
        role_label = self.structural_role or self.metadata_key

        return (
            {
                "type": self.analysis_type or self.metadata_key.title(),
                "sentence": sentence,
                "components": self._to_components(value),
                "analysis": (
                    f"{analysis_label}: {self._describe(value)}"
                ),
                "confidence": float(context.get("confidence", 0.90)),
                "matched_rule": self.display_name,
                "role": role_label,
                "source": self.metadata_key,
            },
        )


class DerivationAwareVakyaRule(_MetadataUpstreamVakyaRule):
    metadata_key = "derivation"
    analysis_type = "DerivationAwareSentence"
    summary_label = "Derivation integrated"
    structural_role = "derivation"

    @property
    def display_name(self) -> str:
        return "Derivation Aware Vakya Rule"

    @property
    def display_description(self) -> str:
        return "Consumes derivation output from context metadata."


class SamasaAwareVakyaRule(_MetadataUpstreamVakyaRule):
    metadata_key = "samasa"
    analysis_type = "SamasaAwareSentence"
    summary_label = "Samasa integrated"
    structural_role = "compound"

    @property
    def display_name(self) -> str:
        return "Samasa Aware Vakya Rule"

    @property
    def display_description(self) -> str:
        return "Consumes samasa output from context metadata."


class SandhiAwareVakyaRule(_MetadataUpstreamVakyaRule):
    metadata_key = "sandhi"
    analysis_type = "SandhiAwareSentence"
    summary_label = "Sandhi integrated"
    structural_role = "phonological_join"

    @property
    def display_name(self) -> str:
        return "Sandhi Aware Vakya Rule"

    @property
    def display_description(self) -> str:
        return "Consumes sandhi output from context metadata."


class GrammarAwareVakyaRule(_MetadataUpstreamVakyaRule):
    metadata_key = "grammar"
    analysis_type = "GrammarAwareSentence"
    summary_label = "Grammar integrated"
    structural_role = "grammar"

    @property
    def display_name(self) -> str:
        return "Grammar Aware Vakya Rule"

    @property
    def display_description(self) -> str:
        return "Consumes grammar output from context metadata."
