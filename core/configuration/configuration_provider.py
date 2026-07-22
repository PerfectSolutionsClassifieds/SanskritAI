from __future__ import annotations

"""
SanskritAI
==========

Configuration Provider

Defines a lightweight mixin for runtime components that expose
an immutable ConfigurationContext.

Components implementing this mixin advertise their active
configuration without revealing how that configuration was
constructed.

Architecture
------------

ConfigurationProvider
        │
        ▼
ConfigurationContext
        │
        ▼
ConfigurationProfile
        │
        ▼
Configuration

Version
-------
v0.6.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.configuration.configuration_context import (
    ConfigurationContext,
)
from SanskritAI.core.configuration.configuration_entry import (
    ConfigurationEntry,
)
from SanskritAI.core.configuration.configuration_key import (
    ConfigurationKey,
)


class ConfigurationProvider(ABC):
    """
    Mixin for components that expose runtime configuration.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def configuration_context(self) -> ConfigurationContext:
        """
        Returns the active runtime configuration context.
        """
        raise NotImplementedError

    @property
    def configuration(self):
        """
        Returns the active configuration.
        """
        return self.configuration_context.configuration

    def contains(
        self,
        key: ConfigurationKey,
    ) -> bool:
        """
        Determines whether the supplied configuration key exists.
        """
        return self.configuration.contains(key)

    def lookup(
        self,
        key: ConfigurationKey,
    ) -> ConfigurationEntry | None:
        """
        Looks up a configuration entry.
        """
        return self.configuration.lookup(key)
