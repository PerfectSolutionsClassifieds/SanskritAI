from __future__ import annotations

"""
SanskritAI
==========

Registry Result

Defines the canonical immutable result returned by Registry
operations.

RegistryResult encapsulates the outcome of registry operations
without relying on exceptions for expected conditions.

Typical operations include:

- register()
- unregister()
- get()
- clear()

Architecture
------------

RegistryStatus
        │
        ▼
RegistryResult

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.registry.registry_entry import RegistryEntry
from SanskritAI.core.registry.registry_exception import RegistryException
from SanskritAI.core.registry.registry_key import RegistryKey
from SanskritAI.core.registry.registry_status import RegistryStatus
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(slots=True, frozen=True)
class RegistryResult(ValueObject):
    """
    Immutable result of a registry operation.
    """

    status: RegistryStatus

    key: RegistryKey | None = None

    entry: RegistryEntry | None = None

    message: str = ""

    exception: RegistryException | None = None

    @property
    def is_success(self) -> bool:
        """
        Returns True if the operation completed successfully.
        """
        return self.status.is_success

    @property
    def is_failure(self) -> bool:
        """
        Returns True if the operation failed.
        """
        return self.status.is_failure

    @property
    def is_informational(self) -> bool:
        """
        Returns True if the operation produced an informational
        status.
        """
        return self.status.is_informational

    @property
    def has_entry(self) -> bool:
        """
        Returns True if an entry is associated with the result.
        """
        return self.entry is not None

    @property
    def has_exception(self) -> bool:
        """
        Returns True if an exception is associated with the
        result.
        """
        return self.exception is not None

    @classmethod
    def success(
        cls,
        status: RegistryStatus,
        *,
        key: RegistryKey | None = None,
        entry: RegistryEntry | None = None,
        message: str = "",
    ) -> "RegistryResult":
        """
        Creates a successful registry result.
        """
        return cls(
            status=status,
            key=key,
            entry=entry,
            message=message,
        )

    @classmethod
    def failure(
        cls,
        status: RegistryStatus,
        *,
        key: RegistryKey | None = None,
        message: str = "",
        exception: RegistryException | None = None,
    ) -> "RegistryResult":
        """
        Creates a failed registry result.
        """
        return cls(
            status=status,
            key=key,
            message=message,
            exception=exception,
        )

    def __bool__(self) -> bool:
        """
        Allows RegistryResult to be used directly in boolean
        contexts.
        """
        return self.is_success
