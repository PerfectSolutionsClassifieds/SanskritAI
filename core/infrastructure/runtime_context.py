from __future__ import annotations

"""
SanskritAI
==========

Runtime Context

Defines the immutable runtime context shared by all
infrastructure components.

A RuntimeContext aggregates the foundational kernels required
for execution but owns no mutable runtime state.

Architecture
------------

ConfigurationRegistry
ServiceContainer
CapabilityRegistry
PluginRegistry
ResourceRegistry
EventDispatcher
        │
        ▼
RuntimeContext
        │
        ▼
RuntimeEnvironment

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.capabilities.capability_registry import CapabilityRegistry
from SanskritAI.core.configuration.configuration_registry import ConfigurationRegistry
from SanskritAI.core.dependency_injection.service_container import ServiceContainer
from SanskritAI.core.events.event_dispatcher import EventDispatcher
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.plugins.plugin_registry import PluginRegistry
from SanskritAI.core.resources.resource_registry import ResourceRegistry
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class RuntimeContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable runtime context.
    """

    configuration: ConfigurationRegistry

    services: ServiceContainer

    capabilities: CapabilityRegistry

    plugins: PluginRegistry

    resources: ResourceRegistry

    events: EventDispatcher

    @property
    def identifier(self) -> str:
        return "runtime_context"

    @property
    def display_name(self) -> str:
        return "Runtime Context"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Immutable snapshot of the runtime "
            "configuration and services."
        )

    def __str__(self) -> str:
        return self.display_text
