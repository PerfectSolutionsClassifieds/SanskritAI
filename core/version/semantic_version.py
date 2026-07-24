from __future__ import annotations

"""
SanskritAI
==========

Semantic Version

Defines an immutable Semantic Version consisting of major,
minor, and patch components.

Unlike the generic Version value object, SemanticVersion
uses composition rather than inheritance. A cached Version
instance is created during initialization.

Architecture
------------

ValueObject
      │
      ▼
SemanticVersion
      │
      └── Version

Version
-------
v0.7.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.core.version.version import Version


@dataclass(frozen=True, slots=True)
class SemanticVersion(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Semantic Version.

    Examples
    --------
    SemanticVersion(1, 0, 0)

    SemanticVersion(2, 5, 13)
    """

    major: int

    minor: int

    patch: int

    _version: Version = field(
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        for name, value in (
            ("major", self.major),
            ("minor", self.minor),
            ("patch", self.patch),
        ):
            if value < 0:
                raise ValueError(
                    f"{name.capitalize()} version cannot be negative."
                )

        object.__setattr__(
            self,
            "_version",
            Version(str(self)),
        )

    @property
    def version(self) -> Version:
        """
        Returns the cached generic Version object.
        """
        return self._version

    @property
    def identifier(self) -> str:
        """
        Returns the canonical semantic version string.
        """
        return self._version.identifier

    @property
    def display_name(self) -> str:
        return self._version.display_name

    @property
    def display_text(self) -> str:
        return self._version.display_text

    @property
    def display_description(self) -> str:
        return (
            f"Semantic Version {self._version}"
        )

    def increment_major(self) -> "SemanticVersion":
        """
        Returns the next major version.
        """
        return SemanticVersion(
            self.major + 1,
            0,
            0,
        )

    def increment_minor(self) -> "SemanticVersion":
        """
        Returns the next minor version.
        """
        return SemanticVersion(
            self.major,
            self.minor + 1,
            0,
        )

    def increment_patch(self) -> "SemanticVersion":
        """
        Returns the next patch version.
        """
        return SemanticVersion(
            self.major,
            self.minor,
            self.patch + 1,
        )

    def __str__(self) -> str:
        return (
            f"{self.major}."
            f"{self.minor}."
            f"{self.patch}"
        )
