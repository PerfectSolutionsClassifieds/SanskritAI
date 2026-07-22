from __future__ import annotations

"""
SanskritAI
==========

Knowledge Identifier

Immutable identifier for structured knowledge resources.

A KnowledgeIdentifier uniquely identifies concepts, ontology
nodes, dictionary entries, synsets, semantic relations, and
other knowledge objects managed by SanskritAI.

This class is intentionally generic and is not tied to any
single knowledge source such as Amarakośa.

Examples
--------
KNOWLEDGE:AMARAKOSHA:SVARGA:001:012

KNOWLEDGE:SHABDAKALPADRUMA:अग्नि

KNOWLEDGE:DHATUPATHA:गम्

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.identities.resource_identifier import (
    ResourceIdentifier,
)


@dataclass(slots=True, frozen=True)
class KnowledgeIdentifier(ResourceIdentifier):
    """
    Identifier for knowledge resources.
    """

    DEFAULT_NAMESPACE: str = "KNOWLEDGE"

    def __post_init__(self) -> None:
        """
        Apply the default knowledge namespace.
        """
        if not self.namespace:
            object.__setattr__(
                self,
                "namespace",
                self.DEFAULT_NAMESPACE,
            )

        super().__post_init__()

    # ---------------------------------------------------------
    # Knowledge Semantics
    # ---------------------------------------------------------

    @property
    def knowledge_source(self) -> str:
        """
        Top-level knowledge source.

        Examples
        --------
        AMARAKOSHA

        SHABDAKALPADRUMA

        VACASPATYAM

        DHATUPATHA
        """
        return self.resource_path[0]

    @property
    def concept_path(self) -> tuple[str, ...]:
        """
        Complete concept hierarchy excluding the namespace.
        """
        return self.resource_path

    @property
    def concept_name(self) -> str:
        """
        Final concept within the hierarchy.
        """
        return self.resource_name

    @property
    def concept_depth(self) -> int:
        """
        Number of hierarchy levels beneath the knowledge source.
        """
        return max(0, self.resource_depth - 1)

    @property
    def concept_location(self) -> tuple[str, ...]:
        """
        Hierarchy beneath the knowledge source.

        Example
        -------
        KNOWLEDGE:AMARAKOSHA:SVARGA:001:012

        ->
        ("SVARGA", "001", "012")
        """
        if self.resource_depth <= 1:
            return ()

        return self.resource_path[1:]

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"source={self.knowledge_source!r}, "
            f"path={self.concept_path!r})"
        )
