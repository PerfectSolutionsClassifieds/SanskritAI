from __future__ import annotations

"""
SanskritAI
==========

Resource Type

Defines the canonical types of resources.

Version
-------
v0.7.0
"""

from enum import Enum
from enum import unique


@unique
class ResourceType(Enum):
    """
    Canonical resource types.
    """

    TEXT = "text"

    JSON = "json"

    XML = "xml"

    YAML = "yaml"

    IMAGE = "image"

    AUDIO = "audio"

    VIDEO = "video"

    PDF = "pdf"

    DATABASE = "database"

    MODEL = "model"

    ARCHIVE = "archive"

    DIRECTORY = "directory"

    CORPUS = "corpus"

    DICTIONARY = "dictionary"

    CACHE = "cache"

    OTHER = "other"

    @property
    def identifier(self) -> str:
        return self.value

    @property
    def display_name(self) -> str:
        return self.value.replace("_", " ").title()

    def __str__(self) -> str:
        return self.display_name
