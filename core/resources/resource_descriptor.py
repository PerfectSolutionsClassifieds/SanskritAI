from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.resources.resource_manifest import ResourceManifest
from SanskritAI.core.resources.resource_metadata import ResourceMetadata
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ResourceDescriptor(
    ValueObject,
    Immutable,
    Displayable,
):

    metadata: ResourceMetadata

    manifest: ResourceManifest

    @property
    def identifier(self) -> str:
        return self.metadata.identifier

    @property
    def display_name(self) -> str:
        return self.metadata.display_name

    @property
    def display_text(self) -> str:
        return self.metadata.display_text

    @property
    def display_description(self) -> str:
        return self.metadata.display_description
