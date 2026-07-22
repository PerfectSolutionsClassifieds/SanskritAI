from __future__ import annotations

"""
SanskritAI
==========

Serialization Format

Defines the canonical serialization formats supported by the
Serialization Kernel.

Serialization formats describe how objects are represented for
exchange or persistence. They are intentionally independent of
storage technologies (PostgreSQL, MongoDB, Redis, etc.).

Version
-------
v0.6.0
"""

from enum import Enum, auto


class SerializationFormat(Enum):
    """
    Supported serialization formats.
    """

    # ---------------------------------------------------------
    # Native Python
    # ---------------------------------------------------------

    DICT = auto()

    # ---------------------------------------------------------
    # Text-based
    # ---------------------------------------------------------

    JSON = auto()

    YAML = auto()

    XML = auto()

    CSV = auto()

    TOML = auto()

    # ---------------------------------------------------------
    # Binary
    # ---------------------------------------------------------

    BSON = auto()

    MESSAGEPACK = auto()

    PICKLE = auto()

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_text(self) -> bool:
        """
        Returns True if the format is text-based.
        """
        return self in {
            SerializationFormat.JSON,
            SerializationFormat.YAML,
            SerializationFormat.XML,
            SerializationFormat.CSV,
            SerializationFormat.TOML,
        }

    @property
    def is_binary(self) -> bool:
        """
        Returns True if the format is binary.
        """
        return self in {
            SerializationFormat.BSON,
            SerializationFormat.MESSAGEPACK,
            SerializationFormat.PICKLE,
        }

    @property
    def is_native(self) -> bool:
        """
        Returns True if the format is Python-native.
        """
        return self is SerializationFormat.DICT

    @property
    def extension(self) -> str:
        """
        Conventional filename extension.
        """
        return {
            SerializationFormat.DICT: "",
            SerializationFormat.JSON: ".json",
            SerializationFormat.YAML: ".yaml",
            SerializationFormat.XML: ".xml",
            SerializationFormat.CSV: ".csv",
            SerializationFormat.TOML: ".toml",
            SerializationFormat.BSON: ".bson",
            SerializationFormat.MESSAGEPACK: ".msgpack",
            SerializationFormat.PICKLE: ".pkl",
        }[self]
