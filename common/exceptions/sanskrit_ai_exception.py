from __future__ import annotations

"""
SanskritAI
==========

Base Exception

Root exception class for the entire SanskritAI project.

All project-specific exceptions should inherit from
SanskritAIException rather than directly from Exception.

Benefits
--------
* Consistent exception hierarchy
* Centralized error handling
* Easier logging
* Future support for structured error codes
* Future localization support

Version
-------
v0.1.0
"""

from __future__ import annotations

from typing import Any


class SanskritAIException(Exception):
    """
    Root exception for SanskritAI.
    """

    def __init__(
        self,
        message: str,
        *,
        cause: Exception | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(message)

        self.message = message
        self.cause = cause
        self.context = context or {}

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:

        return self.message

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r})"
        )

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {

            "type": self.__class__.__name__,

            "message": self.message,

            "cause": (
                repr(self.cause)
                if self.cause is not None
                else None
            ),

            "context": self.context,

        }
