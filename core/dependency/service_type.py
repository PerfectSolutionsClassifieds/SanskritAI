from __future__ import annotations

"""
SanskritAI
==========

Service Type

Defines the canonical immutable semantic classification of a
service managed by the Dependency Injection kernel.

A ServiceType identifies *what kind* of service is being
provided, independently of any concrete implementation.

Typical examples include:

- parser
- tokenizer
- analyzer
- dictionary
- corpus
- translator
- renderer
- ai_backend

A ServiceType is distinct from a ServiceKey:

    ServiceType  → What kind of service is this?
    ServiceKey   → Which concrete implementation is this?

Architecture
------------

ValueObject
      │
      ▼
ServiceType
      │
      ▼
ServiceDescriptor

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ServiceType(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable semantic service classification.
    """

    name: str

    description: str = ""

    def __post_init__(self) -> None:
        normalized = self.name.strip().lower()

        if not normalized:
            raise ValueError(
                "Service type cannot be empty."
            )

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """
        Returns the canonical service type identifier.
        """
        return self.name

    @property
    def display_name(self) -> str:
        """
        Returns the human-readable service type.
        """
        return self.name.replace("_", " ").title()

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.description

    def matches(
        self,
        name: str,
    ) -> bool:
        """
        Determines whether the supplied service type name
        matches this instance.
        """
        return self.name == name.strip().lower()

    def __str__(self) -> str:
        return self.display_name


# ------------------------------------------------------------------
# Canonical Service Types
# ------------------------------------------------------------------

ServiceType.PARSER = ServiceType("parser")
ServiceType.TOKENIZER = ServiceType("tokenizer")
ServiceType.ANALYZER = ServiceType("analyzer")
ServiceType.DICTIONARY = ServiceType("dictionary")
ServiceType.CORPUS = ServiceType("corpus")
ServiceType.TRANSLATOR = ServiceType("translator")
ServiceType.RENDERER = ServiceType("renderer")
ServiceType.AI_BACKEND = ServiceType("ai_backend")
ServiceType.PIPELINE = ServiceType("pipeline")
ServiceType.PLUGIN = ServiceType("plugin")
