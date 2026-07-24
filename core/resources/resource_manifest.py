from __future__ import annotations

from dataclasses import dataclass

from SanskritAI.core.location.location import Location
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ResourceManifest(
    ValueObject,
    Immutable,
    Displayable,
):

    location: Location

    checksum: str = ""

    encoding: str = "utf-8"

    compressed: bool = False

    @property
    def identifier(self) -> str:
        return self.location.identifier

    @property
    def display_name(self) -> str:
        return self.location.display_name

    @property
    def display_text(self) -> str:
        return self.location.display_text

    @property
    def display_description(self) -> str:
        return "Resource Manifest"
