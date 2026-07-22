from __future__ import annotations

"""
SanskritAI
==========

Core Typing

Centralized type aliases and generic type variables used
throughout the SanskritAI Architectural Kernel.

Keeping these definitions in a single location reduces
duplication, improves readability, and minimizes circular
dependencies.

Version
-------
v0.3.0
"""

from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from typing import (
    Any,
    Generic,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Optional,
    Protocol,
    Sequence,
    TypeAlias,
    TypeVar,
)

# ---------------------------------------------------------
# Generic Type Variables
# ---------------------------------------------------------

T = TypeVar("T")
KT = TypeVar("KT")
VT = TypeVar("VT")

TNode = TypeVar("TNode")
TChild = TypeVar("TChild")
TMetadata = TypeVar("TMetadata")
TIdentifier = TypeVar("TIdentifier")

# ---------------------------------------------------------
# Common Type Aliases
# ---------------------------------------------------------

JsonValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | dict[str, "JsonValue"]
    | list["JsonValue"]
)

JsonDict: TypeAlias = dict[str, JsonValue]

PathLike: TypeAlias = str | Path

Attributes: TypeAlias = dict[str, Any]

# ---------------------------------------------------------
# Collection Aliases
# ---------------------------------------------------------

Items: TypeAlias = Iterable[T]
ItemIterator: TypeAlias = Iterator[T]

MappingType: TypeAlias = Mapping[KT, VT]
MutableMappingType: TypeAlias = MutableMapping[KT, VT]

SequenceType: TypeAlias = Sequence[T]
MutableSequenceType: TypeAlias = MutableSequence[T]

MutableSetType: TypeAlias = MutableSet[T]

# ---------------------------------------------------------
# Callable Aliases
# ---------------------------------------------------------

Factory: TypeAlias = Callable[..., T]

Predicate: TypeAlias = Callable[[T], bool]

Transformer: TypeAlias = Callable[[T], T]

Consumer: TypeAlias = Callable[[T], None]

# ---------------------------------------------------------
# Exported Symbols
# ---------------------------------------------------------

__all__ = [
    "T",
    "KT",
    "VT",
    "TNode",
    "TChild",
    "TMetadata",
    "TIdentifier",
    "JsonValue",
    "JsonDict",
    "PathLike",
    "Attributes",
    "Items",
    "ItemIterator",
    "MappingType",
    "MutableMappingType",
    "SequenceType",
    "MutableSequenceType",
    "MutableSetType",
    "Factory",
    "Predicate",
    "Transformer",
    "Consumer",
]
