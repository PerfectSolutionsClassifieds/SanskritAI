from __future__ import annotations

"""
SanskritAI
==========

Semantic Concept Repository

Defines the repository abstraction and a small in-memory
default repository for reusable semantic concepts.

This lets the Semantic Kernel normalize repeated meanings into
stable concept entities instead of re-creating them on every
analysis pass.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.semantic.semantic_concept import SemanticConcept


class SemanticConceptRepository(
    ABC,
    Displayable,
):
    """
    Abstract repository for reusable semantic concepts.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract repository for semantic concepts."

    @abstractmethod
    def get(self, identifier: str) -> SemanticConcept | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_name(self, name: str) -> SemanticConcept | None:
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str) -> tuple[SemanticConcept, ...]:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> tuple[SemanticConcept, ...]:
        raise NotImplementedError

    @abstractmethod
    def contains(self, identifier: str) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError


DEFAULT_SEMANTIC_CONCEPTS: tuple[SemanticConcept, ...] = (
    SemanticConcept(
        identifier="semantic.concept.agent",
        name="Agent",
        gloss="कर्ता",
        category="role",
        description="Entity that performs an action.",
    ),
    SemanticConcept(
        identifier="semantic.concept.patient",
        name="Patient",
        gloss="कर्म",
        category="role",
        description="Entity that undergoes an action.",
    ),
    SemanticConcept(
        identifier="semantic.concept.action",
        name="Action",
        gloss="क्रिया",
        category="event",
        description="Event or action concept.",
    ),
    SemanticConcept(
        identifier="semantic.concept.compound",
        name="Compound",
        gloss="समास",
        category="structure",
        description="Compound linguistic structure.",
    ),
    SemanticConcept(
        identifier="semantic.concept.derivation",
        name="Derivation",
        gloss="प्रत्यय-निर्माण",
        category="structure",
        description="Morphological derivation concept.",
    ),
    SemanticConcept(
        identifier="semantic.concept.sandhi",
        name="Sandhi",
        gloss="संधि",
        category="phonology",
        description="Phonological joining concept.",
    ),
    SemanticConcept(
        identifier="semantic.concept.grammar",
        name="Grammar",
        gloss="व्याकरण",
        category="analysis",
        description="Grammatical analysis concept.",
    ),
    SemanticConcept(
        identifier="semantic.concept.meaning",
        name="Meaning",
        gloss="अर्थ",
        category="semantic",
        description="General meaning concept.",
    ),
)


@dataclass(frozen=True, slots=True)
class DefaultSemanticConceptRepository(
    SemanticConceptRepository,
):
    """
    Small in-memory canonical concept repository.
    """

    concepts: tuple[SemanticConcept, ...] = field(
        default_factory=lambda: DEFAULT_SEMANTIC_CONCEPTS,
    )

    @property
    def display_name(self) -> str:
        return "Default Semantic Concept Repository"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical in-memory repository of semantic concepts."

    def get(self, identifier: str) -> SemanticConcept | None:
        for concept in self.concepts:
            if concept.identifier == identifier:
                return concept
        return None

    def find_by_name(self, name: str) -> SemanticConcept | None:
        needle = name.strip().lower()
        if not needle:
            return None

        for concept in self.concepts:
            if concept.name.lower() == needle:
                return concept
        return None

    def search(self, query: str) -> tuple[SemanticConcept, ...]:
        needle = query.strip().lower()
        if not needle:
            return self.concepts

        return tuple(
            concept
            for concept in self.concepts
            if needle in concept.identifier.lower()
            or needle in concept.name.lower()
            or needle in concept.gloss.lower()
            or needle in concept.category.lower()
            or needle in concept.description.lower()
        )

    def all(self) -> tuple[SemanticConcept, ...]:
        return self.concepts

    def contains(self, identifier: str) -> bool:
        return self.get(identifier) is not None

    @property
    def count(self) -> int:
        return len(self.concepts)
