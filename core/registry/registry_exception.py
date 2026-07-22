from __future__ import annotations

"""
SanskritAI
==========

Registry Exception

Defines the root exception hierarchy for the Registry Kernel.

All registry-related exceptions derive from this class.

Typical subclasses include:

- DuplicateRegistryKeyError
- RegistryKeyNotFoundError
- RegistryEntryDisabledError
- RegistryTypeMismatchError
- ImmutableRegistryError
- RegistryValidationError

Architecture
------------

Exception
      │
      ▼
RegistryException
      │
      ├── DuplicateRegistryKeyError
      ├── RegistryKeyNotFoundError
      ├── RegistryEntryDisabledError
      ├── RegistryTypeMismatchError
      ├── ImmutableRegistryError
      └── RegistryValidationError

Version
-------
v0.6.0
"""

from typing import Any

from SanskritAI.core.registry.registry_key import RegistryKey


class RegistryException(Exception):
    """
    Root exception for the Registry Kernel.
    """

    def __init__(
        self,
        message: str,
        *,
        key: RegistryKey | None = None,
        value: Any | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initializes a registry exception.

        Parameters
        ----------
        message:
            Human-readable error message.

        key:
            Registry key associated with the failure.

        value:
            Optional registry value associated with the failure.

        cause:
            Underlying exception, if any.
        """
        super().__init__(message)

        self._message = message
        self._key = key
        self._value = value
        self._cause = cause

    @property
    def message(self) -> str:
        """
        Returns the error message.
        """
        return self._message

    @property
    def key(self) -> RegistryKey | None:
        """
        Returns the registry key associated with the error.
        """
        return self._key

    @property
    def value(self) -> Any | None:
        """
        Returns the registry value associated with the error.
        """
        return self._value

    @property
    def cause(self) -> Exception | None:
        """
        Returns the underlying cause of the error.
        """
        return self._cause

    @property
    def has_cause(self) -> bool:
        """
        Returns True if an underlying exception exists.
        """
        return self._cause is not None

    def __str__(self) -> str:
        if self._key is None:
            return self._message

        return f"{self._message} [key={self._key}]"
