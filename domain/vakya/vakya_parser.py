from __future__ import annotations

"""
SanskritAI
==========

Vakya Parser

Provides a lightweight sentence parsing and role extraction
layer for the Vakya Kernel.

This module goes beyond simple metadata aggregation by
normalizing the sentence through VakyaStructure and then
extracting a small set of sentence roles from:

    • explicit metadata hints
    • upstream kernel outputs
    • simple heuristic token patterns

The first goal is not to solve full Sanskrit sentence parsing,
but to provide a stable structural layer that can later be
extended into:

    • karaka extraction
    • pada grouping
    • dependency mapping
    • sentence graph construction

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.vakya.vakya_structure import VakyaStructure


@dataclass(frozen=True, slots=True)
class VakyaRole(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    One extracted sentence role or structural label.
    """

    identifier: str

    role: str

    value: Any = None

    source: str = ""

    confidence: float = 1.0

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.role

    @property
    def display_text(self) -> str:
        if self.value is None:
            return self.role
        return f"{self.role}: {self.value}"

    @property
    def display_description(self) -> str:
        return self.notes

    @property
    def has_value(self) -> bool:
        return self.value is not None

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    def __str__(self) -> str:
        return self.display_text


@dataclass(frozen=True, slots=True)
class VakyaParseResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable parse result for a Sanskrit sentence.
    """

    identifier: str

    structure: VakyaStructure

    roles: tuple[VakyaRole, ...] = field(default_factory=tuple)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return "Vakya Parse Result"

    @property
    def display_text(self) -> str:
        return self.structure.normalized_sentence

    @property
    def display_description(self) -> str:
        return "Parsed sentence structure with extracted roles."

    @property
    def role_count(self) -> int:
        return len(self.roles)

    @property
    def has_roles(self) -> bool:
        return self.role_count > 0

    @property
    def first_role(self) -> VakyaRole | None:
        if not self.roles:
            return None
        return self.roles[0]

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def __iter__(self) -> Iterator[VakyaRole]:
        return iter(self.roles)

    def __len__(self) -> int:
        return len(self.roles)

    def __getitem__(self, index: int) -> VakyaRole:
        return self.roles[index]

    def __str__(self) -> str:
        return self.display_text


class VakyaParser:
    """
    Lightweight sentence parser and role extractor.

    The parser operates on a VakyaStructure and yields a
    VakyaParseResult.
    """

    _ROLE_HINT_KEYS: tuple[str, ...] = (
        "role",
        "roles",
        "karaka",
        "karakas",
        "subject",
        "object",
        "predicate",
        "agent",
        "patient",
        "action",
    )

    _ROLE_ALIASES: dict[str, str] = {
        "कर्ता": "subject",
        "kartā": "subject",
        "karta": "subject",
        "subject": "subject",
        "कर्म": "object",
        "karma": "object",
        "object": "object",
        "क्रिया": "predicate",
        "kriya": "predicate",
        "predicate": "predicate",
        "verb": "predicate",
        "agent": "agent",
        "patient": "patient",
        "action": "action",
        "karaka": "karaka",
    }

    @staticmethod
    def _as_tuple(value: Any) -> tuple[Any, ...]:
        if value is None:
            return tuple()
        if isinstance(value, tuple):
            return value
        if isinstance(value, list):
            return tuple(value)
        return (value,)

    def _extract_hint_roles(self, metadata: dict[str, Any]) -> list[VakyaRole]:
        roles: list[VakyaRole] = []

        for key in self._ROLE_HINT_KEYS:
            if key not in metadata:
                continue

            value = metadata[key]
            values = self._as_tuple(value)

            for index, item in enumerate(values, start=1):
                role_name = self._ROLE_ALIASES.get(
                    str(key).lower(),
                    str(key).lower(),
                )

                if isinstance(item, dict):
                    role_name = str(
                        item.get("role", role_name)
                    ).strip() or role_name
                    role_value = item.get("value", item)
                    confidence = float(item.get("confidence", 0.90))
                    notes = str(item.get("notes", "")).strip()
                else:
                    role_value = item
                    confidence = 0.90
                    notes = ""

                roles.append(
                    VakyaRole(
                        identifier=f"hint:{key}:{index}",
                        role=role_name,
                        value=role_value,
                        source="metadata",
                        confidence=confidence,
                        notes=notes,
                    )
                )

        return roles

    def _extract_upstream_roles(
        self,
        metadata: dict[str, Any],
    ) -> list[VakyaRole]:
        roles: list[VakyaRole] = []

        for key in ("derivation", "samasa", "sandhi", "grammar"):
            if key not in metadata:
                continue

            value = metadata[key]
            confidence = 0.92

            if hasattr(value, "display_text"):
                text = str(value.display_text)
            else:
                text = str(value)

            roles.append(
                VakyaRole(
                    identifier=f"upstream:{key}",
                    role=key,
                    value=text,
                    source="upstream",
                    confidence=confidence,
                    notes=f"Derived from {key} output.",
                )
            )

        return roles

    def _extract_token_roles(
        self,
        structure: VakyaStructure,
    ) -> list[VakyaRole]:
        roles: list[VakyaRole] = []

        tokens = structure.components

        if not tokens:
            return roles

        if len(tokens) == 1:
            roles.append(
                VakyaRole(
                    identifier="token:1",
                    role="sentence",
                    value=tokens[0],
                    source="heuristic",
                    confidence=0.75,
                    notes="Single-token sentence heuristic.",
                )
            )
            return roles

        # Very light heuristic:
        # first token = potential subject/agent
        # last token = potential predicate/action
        roles.append(
            VakyaRole(
                identifier="token:subject",
                role="subject",
                value=tokens[0],
                source="heuristic",
                confidence=0.70,
                notes="First-token sentence heuristic.",
            )
        )

        roles.append(
            VakyaRole(
                identifier="token:predicate",
                role="predicate",
                value=tokens[-1],
                source="heuristic",
                confidence=0.70,
                notes="Last-token sentence heuristic.",
            )
        )

        if len(tokens) >= 3:
            roles.append(
                VakyaRole(
                    identifier="token:middle",
                    role="context",
                    value=tokens[1:-1],
                    source="heuristic",
                    confidence=0.60,
                    notes="Middle-token sentence context heuristic.",
                )
            )

        return roles

    def parse(
        self,
        identifier: str,
        sentence: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> VakyaParseResult:
        """
        Parses a raw sentence into a normalized structure and
        extracts a lightweight role set.
        """
        meta = dict(metadata or {})

        structure = VakyaStructure.normalize(
            identifier=identifier,
            sentence=sentence,
            metadata=meta,
        )

        roles: list[VakyaRole] = []
        roles.extend(self._extract_hint_roles(structure.metadata))
        roles.extend(self._extract_upstream_roles(structure.metadata))
        roles.extend(self._extract_token_roles(structure))

        # Preserve order while removing duplicate role/value pairs.
        deduped: list[VakyaRole] = []
        seen: set[tuple[str, str]] = set()

        for role in roles:
            key = (role.role, str(role.value))
            if key in seen:
                continue
            seen.add(key)
            deduped.append(role)

        result_metadata = dict(structure.metadata)
        result_metadata["role_count"] = len(deduped)
        result_metadata["role_names"] = tuple(role.role for role in deduped)

        return VakyaParseResult(
            identifier=identifier,
            structure=structure,
            roles=tuple(deduped),
            metadata=result_metadata,
        )
