"""
Corpus interfaces.

These lightweight protocols define the public contracts shared
across the Canonical Corpus Model.
"""

from .identifiable import Identifiable
from .serializable import Serializable
from .hierarchical import Hierarchical
from .metadata_provider import MetadataProvider
from .node_container import NodeContainer

__all__ = [
    "Identifiable",
    "Serializable",
    "Hierarchical",
    "MetadataProvider",
    "NodeContainer",
]
