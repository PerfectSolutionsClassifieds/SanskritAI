from __future__ import annotations

"""
SanskritAI
==========

Reader Node

Defines the immutable base object for the Reader Domain.

Every object displayed by the Reader UI derives from ReaderNode.

Hierarchy
---------

ReaderNode
    │
    ├── ReaderDocument
    ├── ChapterView
    ├── SlokaView
    └── WordView

Purpose
-------

ReaderNode supplies the common navigation and display
behaviour shared by all reader-facing objects while remaining
completely independent from the linguistic kernels.

The linguistic information is attached separately through
ResolutionResult objects.

Version
-------
v1.0.0
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Any


from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ReaderNode(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Immutable base class for every Reader UI object.
    """

    identifier: str

    title: str = ""

    parent_identifier: str | None = None

    children: tuple[str, ...] = field(
        default_factory=tuple,
    )

    sequence: int = 0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    notes: str = ""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.title or self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.notes

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    @property
    def has_parent(self) -> bool:
        return self.parent_identifier is not None

    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    @property
    def child_count(self) -> int:
        return len(self.children)

    @property
    def is_root(self) -> bool:
        return not self.has_parent

    @property
    def is_leaf(self) -> bool:
        return not self.has_children

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def has_metadata(self) -> bool:
        return bool(self.metadata)

    def metadata_value(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Returns a metadata value.
        """
        return self.metadata.get(
            key,
            default,
        )

    # ---------------------------------------------------------
    # Ordering
    # ---------------------------------------------------------

    def sort_key(self) -> tuple[int, str]:
        """
        Canonical ordering key.
        """
        return (
            self.sequence,
            self.identifier,
        )

    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.child_count

    def __iter__(self):
        return iter(self.children)

    def __contains__(
        self,
        identifier: str,
    ) -> bool:
        return identifier in self.children

    def __str__(self) -> str:
        return self.display_text
