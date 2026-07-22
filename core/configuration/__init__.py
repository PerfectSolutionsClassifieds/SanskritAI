"""
SanskritAI
==========

Configuration Kernel

Defines the immutable configuration model used throughout the
SanskritAI architecture.

Configuration describes *how components behave* at runtime.

Unlike Capabilities, which describe *what components can do*,
Configuration specifies *how those capabilities are enabled,
customized, and controlled*.

Architecture
------------

ConfigurationKey
        │
        ▼
ConfigurationEntry
        │
        ▼
Configuration
        │
        ▼
ConfigurationProfile

Version
-------
v0.6.0
"""

from .configuration_key import ConfigurationKey
from .configuration_value import ConfigurationValue
from .configuration_entry import ConfigurationEntry
from .configuration import Configuration
from .configuration_profile import ConfigurationProfile
from .configuration_provider import ConfigurationProvider
from .configuration_registry import ConfigurationRegistry

__all__ = [
    "ConfigurationKey",
    "ConfigurationValue",
    "ConfigurationEntry",
    "Configuration",
    "ConfigurationProfile",
    "ConfigurationProvider",
    "ConfigurationRegistry",
]
