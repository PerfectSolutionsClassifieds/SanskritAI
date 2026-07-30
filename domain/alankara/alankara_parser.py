from __future__ import annotations

"""
SanskritAI
==========

Alankara Parser

Provides a lightweight normalization and heuristic parsing
layer for the Alankara Kernel.

The parser normalizes the input text and extracts a small set
of candidate stylistic cues before the main Alankara rules run.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
import re
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


_PUNCT_RE = re.compile(r"[।॥!?;:,]")


@dataclass(frozen=True, slots=True)
class AlankaraStructure(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable normalized Alankara input structure.
    """

    identifier: str

    original_text: str

    normalized_text: str

    tokens: tuple[str, ...] = field(default_factory=tuple)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return "Alankara Structure"

    @property
    def display_text(self) -> str:
        return self.normalized_text

    @property
    def display_description(self) -> str:
        return "Normalized Alankara input structure."

    @property
    def token_count(self) -> int:
        return len(self.tokens)

    @property
    def has_tokens(self) -> bool:
        return self.token_count > 0

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def __iter__(self) -> Iterator[str]:
        return iter(self.tokens)

    def __len__(self) -> int:
        return len(self.tokens)

    def __getitem__(self, index: int) -> str:
        return self.tokens[index]

    def __str__(self) -> str:
        return self.display_text

    @classmethod
    def normalize(
        cls,
        identifier: str,
        text: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> "AlankaraStructure":
        """
        Normalizes raw input text for Alankara analysis.
        """
        raw = "" if text is None else str(text)
        trimmed = raw.strip()
        collapsed = re.sub(r"\s+", " ", trimmed)
        punctuation_free = _PUNCT_RE.sub(" ", collapsed)
        normalized = re.sub(r"\s+", " ", punctuation_free).strip()

        tokens = tuple(token for token in normalized.split(" ") if token)

        meta = dict(metadata or {})
        meta.setdefault("original_length", len(raw))
        meta.setdefault("normalized_length", len(normalized))
        meta.setdefault("token_count", len(tokens))
        meta.setdefault("punctuation_removed", normalized != collapsed)

        return cls(
            identifier=identifier,
            original_text=raw,
            normalized_text=normalized,
            tokens=tokens,
            metadata=meta,
        )


@dataclass(frozen=True, slots=True)
class AlankaraParseResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Parsed Alankara input together with lightweight heuristic cues.
    """

    identifier: str

    structure: AlankaraStructure

    cues: tuple[str, ...] = field(default_factory=tuple)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return "Alankara Parse Result"

    @property
    def display_text(self) -> str:
        return self.structure.normalized_text

    @property
    def display_description(self) -> str:
        return "Parsed Alankara structure with heuristic cues."

    @property
    def cue_count(self) -> int:
        return len(self.cues)

    @property
    def has_cues(self) -> bool:
        return self.cue_count > 0

    @property
    def first_cue(self) -> str | None:
        if not self.cues:
            return None
        return self.cues[0]

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def __iter__(self) -> Iterator[str]:
        return iter(self.cues)

    def __len__(self) -> int:
        return len(self.cues)

    def __getitem__(self, index: int) -> str:
        return self.cues[index]

    def __str__(self) -> str:
        return self.display_text


class AlankaraParser:
    """
    Lightweight Alankara normalizer and heuristic parser.
    """

    _MARKERS: dict[str, tuple[str, ...]] = {
        "upamā": ("इव", "यथा", "सदृश", "तुल्य", "like", "as"),
        "rūpaka": ("रूपक", "is", "as if", "ivana"),
        "anuprāsa": ("अनुप्रास",),
        "yamaka": ("यमक",),
        "śleṣa": ("श्लेष", "multiple meanings", "double"),
    }

    def normalize(
        self,
        identifier: str,
        text: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> AlankaraStructure:
        return AlankaraStructure.normalize(
            identifier=identifier,
            text=text,
            metadata=metadata,
        )

    def _extract_cues(self, text: str, metadata: dict[str, Any]) -> list[str]:
        lower = text.lower()
        cues: list[str] = []

        for name, markers in self._MARKERS.items():
            if any(marker.lower() in lower for marker in markers):
                cues.append(name)

        hint = str(metadata.get("alankara_hint", "")).strip().lower()
        if hint:
            cues.append(hint)

        if len(text.split()) >= 2:
            cues.append("verse-like")

        return cues

    def parse(
        self,
        identifier: str,
        text: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> AlankaraParseResult:
        meta = dict(metadata or {})
        structure = self.normalize(
            identifier=identifier,
            text=text,
            metadata=meta,
        )

        cues = self._extract_cues(
            structure.normalized_text,
            structure.metadata,
        )

        result_metadata = dict(structure.metadata)
        result_metadata["cue_count"] = len(cues)
        result_metadata["cue_names"] = tuple(cues)

        return AlankaraParseResult(
            identifier=identifier,
            structure=structure,
            cues=tuple(cues),
            metadata=result_metadata,
        )
