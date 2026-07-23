from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.resources.resource_descriptor import ResourceDescriptor
from SanskritAI.core.resources.resource_registry import ResourceRegistry
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ResourceLocator(
    ValueObject,
    Immutable,
    Displayable,
):

    registry: ResourceRegistry

    @property
    def identifier(self) -> str:
        return "resource_locator"

    @property
    def display_name(self) -> str:
        return "Resource Locator"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Locates registered resources."

    def locate(
        self,
        identifier: str,
    ) -> ResourceDescriptor | None:
        return self.registry.lookup(identifier)
