from __future__ import annotations

"""
SanskritAI
==========

Acquisition Exceptions

Exceptions raised during corpus discovery,
repository access, downloading and acquisition.
"""

from SanskritAI.common.exceptions.sanskrit_ai_exception import (
    SanskritAIException,
)


class AcquisitionException(SanskritAIException):
    """
    Base exception for acquisition subsystem.
    """
    pass


class DiscoveryException(AcquisitionException):
    """
    Raised when corpus discovery fails.
    """
    pass


class RepositoryException(AcquisitionException):
    """
    Raised when repository access fails.
    """
    pass


class DownloadException(AcquisitionException):
    """
    Raised when downloading a resource fails.
    """
    pass


class ProviderException(AcquisitionException):
    """
    Raised by acquisition providers.
    """
    pass
