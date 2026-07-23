from __future__ import annotations

"""
SanskritAI
==========

Plugin State

Defines the lifecycle state of a plugin.

Architecture
------------

Enum
 │
 ▼
PluginState

Version
-------
v0.7.0
"""

from enum import Enum
from enum import unique


@unique
class PluginState(Enum):
    """
    Canonical lifecycle states of a plugin.
    """

    REGISTERED = "registered"

    DISCOVERED = "discovered"

    LOADED = "loaded"

    INITIALIZED = "initialized"

    ENABLED = "enabled"

    DISABLED = "disabled"

    FAILED = "failed"

    UNLOADED = "unloaded"

    @property
    def identifier(self) -> str:
        """
        Returns the canonical state identifier.
        """
        return self.value

    @property
    def display_name(self) -> str:
        """
        Returns a human-readable state name.
        """
        return self.value.replace("_", " ").title()

    @property
    def is_active(self) -> bool:
        """
        Indicates whether the plugin is operational.
        """
        return self in (
            PluginState.LOADED,
            PluginState.INITIALIZED,
            PluginState.ENABLED,
        )

    @property
    def is_terminal(self) -> bool:
        """
        Indicates whether the state is terminal.
        """
        return self in (
            PluginState.FAILED,
            PluginState.UNLOADED,
        )

    def __str__(self) -> str:
        return self.display_name
