from __future__ import annotations

"""
SanskritAI
==========

Vakya Structure

Provides a lightweight normalization layer for sentence inputs
before Vakya rules run.

The goal is to convert raw sentence text into a consistent
structure containing:

    • normalized sentence text
    • token-like sentence components
    • punctuation-aware cleanup
    • simple metadata for downstream rules

This keeps the Vakya Kernel clean and prepares the input for
sentence-analysis rules that consume upstream outputs from
Derivation, Samasa, Sandhi, and Grammar.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
import re
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


_SENTENCE_PUNCTUATION_RE = re.compile(r"[।॥!?;:,]")


@dataclass(frozen=True, slots=True)
class VakyaStructure(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable normalized sentence structure.
    """

    identifier: str

    original_sentence: str

    normalized_sentence: str

    components: tuple[str, ...] = field(default_factory=tuple)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return "Vakya Structure"

    @property
    def display_text(self) -> str:
        return self.normalized_sentence

    @property
    def display_description(self) -> str:
        return "Normalized sentence structure."

    @property
    def component_count(self) -> int:
        return len(self.components)

    @property
    def has_components(self) -> bool:
        return self.component_count > 0

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def __str__(self) -> str:
        return self.display_text

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    @classmethod
    def normalize(
        cls,
        identifier: str,
        sentence: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> "VakyaStructure":
        """
        Normalizes raw sentence text into a stable structure.

        The normalization currently performs:
            • trimming whitespace
            • collapsing repeated spaces
            • removing common danda/punctuation marks from
              token boundaries
            • preserving the original sentence
        """

        raw = "" if sentence is None else str(sentence)
        trimmed = raw.strip()

        # Collapse repeated whitespace while preserving the
        # original word order.
        collapsed = re.sub(r"\s+", " ", trimmed)

        # Remove common sentence punctuation for components.
        punctuation_free = _SENTENCE_PUNCTUATION_RE.sub(" ", collapsed)

        # Collapse whitespace again after punctuation removal.
        normalized = re.sub(r"\s+", " ", punctuation_free).strip()

        components = tuple(
            token
            for token in normalized.split(" ")
            if token
        )

        meta = dict(metadata or {})
        meta.setdefault("original_length", len(raw))
        meta.setdefault("normalized_length", len(normalized))
        meta.setdefault("component_count", len(components))
        meta.setdefault("punctuation_removed", normalized != collapsed)

        return cls(
            identifier=identifier,
            original_sentence=raw,
            normalized_sentence=normalized,
            components=components,
            metadata=meta,
        )

    @classmethod
    def from_sentence(
        cls,
        identifier: str,
        sentence: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> "VakyaStructure":
        """
        Alias for normalize(), kept for readability at call sites.
        """
        return cls.normalize(
            identifier=identifier,
            sentence=sentence,
            metadata=metadata,
        )
