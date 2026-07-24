from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.registry.hierarchical_registry import HierarchicalRegistry
from SanskritAI.core.resources.resource_descriptor import ResourceDescriptor
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ResourceRegistry(
    ValueObject,
    Immutable,
    Displayable,
):

    registry: HierarchicalRegistry[ResourceDescriptor]

    @property
    def identifier(self) -> str:
        return "resource_registry"

    @property
    def display_name(self) -> str:
        return "Resource Registry"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Registry of resources."

    def lookup(
        self,
        identifier: str,
    ) -> ResourceDescriptor | None:
        return self.registry.lookup(identifier)
