from __future__ import annotations

"""
SanskritAI
==========

Registry Exceptions

Exceptions related to registry
operations throughout SanskritAI.
"""

from SanskritAI.common.exceptions.sanskrit_ai_exception import (
    SanskritAIException,
)


class RegistryException(SanskritAIException):
    """
    Base registry exception.
    """
    pass


class DuplicateRegistrationException(RegistryException):
    """
    Raised when attempting to register
    an object more than once.
    """
    pass


class RegistrationNotFoundException(RegistryException):
    """
    Raised when a requested registration
    does not exist.
    """
    pass


class InvalidRegistrationException(RegistryException):
    """
    Raised when an invalid object is
    registered.
    """
    pass
