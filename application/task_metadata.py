from __future__ import annotations

"""
SanskritAI
==========

Task Metadata

Defines the immutable semantic metadata describing an atomic
application task.

TaskMetadata specializes WorkMetadata by introducing task-
specific execution characteristics while remaining completely
declarative.

Architecture
------------

WorkMetadata
      │
      ▼
TaskMetadata
      │
      ▼
Task

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.application.work_metadata import WorkMetadata
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable


@dataclass(frozen=True, slots=True)
class TaskMetadata(
    WorkMetadata,
    Immutable,
    Displayable,
):
    """
    Immutable metadata describing an atomic task.
    """

    atomic: bool = True

    interruptible: bool = False

    retryable: bool = False

    @property
    def display_description(self) -> str:
        parts = []

        if self.description:
            parts.append(self.description)

        properties = []

        if self.atomic:
            properties.append("atomic")

        if self.interruptible:
            properties.append("interruptible")

        if self.retryable:
            properties.append("retryable")

        if properties:
            parts.append(
                f"Properties: {', '.join(properties)}."
            )

        return " ".join(parts)
