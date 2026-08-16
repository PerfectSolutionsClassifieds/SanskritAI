from __future__ import annotations

"""
SanskritAI
==========

Lexical Source
--------------

Defines the domain representation of a lexical knowledge source.

A LexicalSource represents the provenance of lexical information,
such as Amarakośa, Dhātupāṭha, Monier-Williams, Apte,
Vācaspatyam, Śabdakalpadruma, or Sanskrit Heritage.

The canonical DictionarySource enum is reused from the existing
SanskritAI enum layer.

Version
-------

v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.models.enums.dictionary_source import DictionarySource


@dataclass(frozen=True, slots=True)
class LexicalSource(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable lexical knowledge source.

    Parameters
    ----------
    source_id:
        Stable identifier for the source.

    name:
        Human-readable source name.

    source_type:
        Canonical DictionarySource classification.

    version:
        Optional edition or version identifier.

    language:
        Language associated with the source.

    script:
        Primary script associated with the source.

    description:
        Human-readable description.

    url:
        Optional external reference URL.
    """

    source_id: str
    name: str
    source_type: DictionarySource = DictionarySource.UNKNOWN
    version: str = ""
    language: str = "sanskrit"
    script: str = "devanagari"
    description: str = ""
    url: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_id",
            self.source_id.strip(),
        )
        object.__setattr__(
            self,
            "name",
            self.name.strip(),
        )
        object.__setattr__(
            self,
            "version",
            self.version.strip(),
        )
        object.__setattr__(
            self,
            "language",
            self.language.strip(),
        )
        object.__setattr__(
            self,
            "script",
            self.script.strip(),
        )
        object.__setattr__(
            self,
            "description",
            self.description.strip(),
        )
        object.__setattr__(
            self,
            "url",
            self.url.strip(),
        )

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        if self.version:
            return f"{self.name} ({self.version})"

        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def has_version(self) -> bool:
        return bool(self.version)

    @property
    def has_description(self) -> bool:
        return bool(self.description)

    @property
    def has_url(self) -> bool:
        return bool(self.url)

    @property
    def canonical_name(self) -> str:
        return self.source_type.value

    def to_dict(self) -> dict[str, str]:
        return {
            "source_id": self.source_id,
            "name": self.name,
            "source_type": self.source_type.value,
            "version": self.version,
            "language": self.language,
            "script": self.script,
            "description": self.description,
            "url": self.url,
        }

    def __str__(self) -> str:
        return self.display_text
