from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.core.location.location import Location
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.resources.resource_id import ResourceId
from SanskritAI.core.resources.resource_state import ResourceState
from SanskritAI.core.resources.resource_type import ResourceType
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ResourceMetadata(
    ValueObject,
    Immutable,
    Displayable,
):

    resource_id: ResourceId

    resource_type: ResourceType

    state: ResourceState

    location: Location

    description: str = ""

    @property
    def identifier(self) -> str:
        return self.resource_id.identifier

    @property
    def display_name(self) -> str:
        return self.resource_id.display_name

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.description
