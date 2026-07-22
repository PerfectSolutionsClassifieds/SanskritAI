
from __future__ import annotations

"""
SanskritAI
==========

Acquisition Source Licenses

Defines the licensing model associated with an acquisition
source. This information is preserved as metadata and is used
by the acquisition framework to determine whether a source
may be downloaded, cached, redistributed, or published.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from enum import Enum


class SourceLicense(str, Enum):
    """
    License associated with an acquisition source.
    """

    # Public Domain
    PUBLIC_DOMAIN = "public_domain"

    # Creative Commons
    CC0 = "cc0"
    CC_BY = "cc_by"
    CC_BY_SA = "cc_by_sa"
    CC_BY_NC = "cc_by_nc"
    CC_BY_NC_SA = "cc_by_nc_sa"

    # Open Data
    OPEN_DATA = "open_data"

    # MIT
    MIT = "mit"

    # Apache
    APACHE_2 = "apache_2"

    # BSD
    BSD = "bsd"

    # GPL
    GPL = "gpl"

    # LGPL
    LGPL = "lgpl"

    # Proprietary
    PROPRIETARY = "proprietary"

    # Membership / subscription
    RESTRICTED = "restricted"

    # Research use only
    RESEARCH = "research"

    # Unknown
    UNKNOWN = "unknown"

    @property
    def is_open(self) -> bool:
        """
        Returns True if the source is considered openly usable.
        """
        return self in {
            SourceLicense.PUBLIC_DOMAIN,
            SourceLicense.CC0,
            SourceLicense.CC_BY,
            SourceLicense.CC_BY_SA,
            SourceLicense.OPEN_DATA,
            SourceLicense.MIT,
            SourceLicense.APACHE_2,
            SourceLicense.BSD,
        }

    @property
    def requires_attribution(self) -> bool:
        """
        Returns True if attribution is generally required.
        """
        return self in {
            SourceLicense.CC_BY,
            SourceLicense.CC_BY_SA,
            SourceLicense.CC_BY_NC,
            SourceLicense.CC_BY_NC_SA,
        }

    @property
    def allows_commercial_use(self) -> bool:
        """
        Returns True if commercial use is generally permitted.
        """
        return self in {
            SourceLicense.PUBLIC_DOMAIN,
            SourceLicense.CC0,
            SourceLicense.CC_BY,
            SourceLicense.CC_BY_SA,
            SourceLicense.OPEN_DATA,
            SourceLicense.MIT,
            SourceLicense.APACHE_2,
            SourceLicense.BSD,
        }

    @property
    def requires_permission(self) -> bool:
        """
        Returns True if explicit permission or membership
        is typically required.
        """
        return self in {
            SourceLicense.PROPRIETARY,
            SourceLicense.RESTRICTED,
            SourceLicense.RESEARCH,
            SourceLicense.UNKNOWN,
        }

    @classmethod
    def from_string(cls, value: str) -> "SourceLicense":
        """
        Parse a string into a SourceLicense.

        Unknown values return SourceLicense.UNKNOWN.
        """
        normalized = value.strip().lower()

        for member in cls:
            if member.value == normalized:
                return member

        return cls.UNKNOWN

    def __str__(self) -> str:
        return self.value
