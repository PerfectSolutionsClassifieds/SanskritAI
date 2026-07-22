from __future__ import annotations

"""
SanskritAI
==========

Registry Status

Defines the canonical status values representing the outcome
or lifecycle state of Registry operations.

RegistryStatus is shared by RegistryResult, diagnostics,
logging, and future infrastructure services.

Typical operations include:

- register()
- unregister()
- get()
- clear()

Version
-------
v0.6.0
"""

from enum import Enum


class RegistryStatus(str, Enum):
    """
    Canonical registry operation status.
    """

    # ---------------------------------------------------------
    # Successful operations
    # ---------------------------------------------------------

    REGISTERED = "registered"

    UPDATED = "updated"

    REMOVED = "removed"

    FOUND = "found"

    CLEARED = "cleared"

    # ---------------------------------------------------------
    # Informational
    # ---------------------------------------------------------

    ALREADY_REGISTERED = "already_registered"

    NOT_FOUND = "not_found"

    DISABLED = "disabled"

    EMPTY = "empty"

    # ---------------------------------------------------------
    # Failure
    # ---------------------------------------------------------

    INVALID_KEY = "invalid_key"

    INVALID_ENTRY = "invalid_entry"

    TYPE_MISMATCH = "type_mismatch"

    IMMUTABLE = "immutable"

    ERROR = "error"

    @property
    def is_success(self) -> bool:
        """
        Returns True if this status represents a successful
        registry operation.
        """
        return self in {
            RegistryStatus.REGISTERED,
            RegistryStatus.UPDATED,
            RegistryStatus.REMOVED,
            RegistryStatus.FOUND,
            RegistryStatus.CLEARED,
        }

    @property
    def is_failure(self) -> bool:
        """
        Returns True if this status represents a failed
        registry operation.
        """
        return self in {
            RegistryStatus.INVALID_KEY,
            RegistryStatus.INVALID_ENTRY,
            RegistryStatus.TYPE_MISMATCH,
            RegistryStatus.IMMUTABLE,
            RegistryStatus.ERROR,
        }

    @property
    def is_informational(self) -> bool:
        """
        Returns True if this status represents an informational
        (non-error) state.
        """
        return self in {
            RegistryStatus.ALREADY_REGISTERED,
            RegistryStatus.NOT_FOUND,
            RegistryStatus.DISABLED,
            RegistryStatus.EMPTY,
        }
