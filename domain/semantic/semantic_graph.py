from __future__ import annotations

"""
SanskritAI
==========

Semantic Graph

Represents a structured semantic network composed of concepts,
relations, and frames.

The SemanticGraph is the unifying container for the Semantic
Kernel. It allows meaning to be represented as a graph of
reusable concepts connected by labeled relations, with optional
semantic frames for higher-level interpretation.

This object is intended to support:
    • concept normalization
    • relation extraction
    • frame assembly
    • meaning network merging
    • future ontology and knowledge-graph integration

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.semantic.semantic_concept import SemanticConcept
from SanskritAI.domain.semantic.semantic_frame import SemanticFrame
from SanskritAI.domain.semantic.semantic_relation import SemanticRelation


@dataclass(frozen=True, slots=True)
class SemanticGraph(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable semantic graph composed of concepts, relations
    and frames.
    """

    identifier: str

    concepts: tuple[SemanticConcept, ...] = field(default_factory=tuple)

    relations: tuple[SemanticRelation, ...] = field(default_factory=tuple)

    frames: tuple[SemanticFrame, ...] = field(default_factory=tuple)

    label: str = ""

    description: str = ""

    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return self.label or "Semantic Graph"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def concept_count(self) -> int:
        return len(self.concepts)

    @property
    def relation_count(self) -> int:
        return len(self.relations)

    @property
    def frame_count(self) -> int:
        return len(self.frames)

    @property
    def is_empty(self) -> bool:
        return (
            self.concept_count == 0
            and self.relation_count == 0
            and self.frame_count == 0
        )

    @property
    def has_concepts(self) -> bool:
        return self.concept_count > 0

    @property
    def has_relations(self) -> bool:
        return self.relation_count > 0

    @property
    def has_frames(self) -> bool:
        return self.frame_count > 0

    @property
    def first_concept(self) -> SemanticConcept | None:
        if not self.concepts:
            return None
        return self.concepts[0]

    @property
    def first_relation(self) -> SemanticRelation | None:
        if not self.relations:
            return None
        return self.relations[0]

    @property
    def first_frame(self) -> SemanticFrame | None:
        if not self.frames:
            return None
        return self.frames[0]

    def get_concept(self, identifier: str) -> SemanticConcept | None:
        for concept in self.concepts:
            if concept.identifier == identifier:
                return concept
        return None

    def get_relation(self, identifier: str) -> SemanticRelation | None:
        for relation in self.relations:
            if relation.identifier == identifier:
                return relation
        return None

    def get_frame(self, identifier: str) -> SemanticFrame | None:
        for frame in self.frames:
            if frame.identifier == identifier:
                return frame
        return None

    def find_concept_by_name(self, name: str) -> SemanticConcept | None:
        needle = name.strip().lower()
        if not needle:
            return None

        for concept in self.concepts:
            if concept.name.lower() == needle:
                return concept
        return None

    def concepts_by_category(self, category: str) -> tuple[SemanticConcept, ...]:
        needle = category.strip().lower()
        if not needle:
            return tuple()

        return tuple(
            concept
            for concept in self.concepts
            if concept.category.lower() == needle
        )

    def relations_by_type(self, relation_type: str) -> tuple[SemanticRelation, ...]:
        needle = relation_type.strip().lower()
        if not needle:
            return tuple()

        return tuple(
            relation
            for relation in self.relations
            if relation.relation.lower() == needle
        )

    def add_concept(self, concept: SemanticConcept) -> "SemanticGraph":
        if self.get_concept(concept.identifier) is not None:
            return self

        return SemanticGraph(
            identifier=self.identifier,
            concepts=self.concepts + (concept,),
            relations=self.relations,
            frames=self.frames,
            label=self.label,
            description=self.description,
            metadata=dict(self.metadata),
        )

    def add_relation(self, relation: SemanticRelation) -> "SemanticGraph":
        if self.get_relation(relation.identifier) is not None:
            return self

        concepts = self.concepts
        if self.get_concept(relation.source.identifier) is None:
            concepts = concepts + (relation.source,)
        if self.get_concept(relation.target.identifier) is None:
            concepts = concepts + (relation.target,)

        return SemanticGraph(
            identifier=self.identifier,
            concepts=concepts,
            relations=self.relations + (relation,),
            frames=self.frames,
            label=self.label,
            description=self.description,
            metadata=dict(self.metadata),
        )

    def add_frame(self, frame: SemanticFrame) -> "SemanticGraph":
        if self.get_frame(frame.identifier) is not None:
            return self

        concepts = self.concepts
        relations = self.relations

        for concept in frame.concepts:
            if self.get_concept(concept.identifier) is None:
                concepts = concepts + (concept,)

        for relation in frame.relations:
            if self.get_relation(relation.identifier) is None:
                relations = relations + (relation,)
            if self.get_concept(relation.source.identifier) is None:
                concepts = concepts + (relation.source,)
            if self.get_concept(relation.target.identifier) is None:
                concepts = concepts + (relation.target,)

        return SemanticGraph(
            identifier=self.identifier,
            concepts=concepts,
            relations=relations,
            frames=self.frames + (frame,),
            label=self.label,
            description=self.description,
            metadata=dict(self.metadata),
        )

    def merge(self, other: "SemanticGraph") -> "SemanticGraph":
        graph = self

        for concept in other.concepts:
            graph = graph.add_concept(concept)

        for relation in other.relations:
            graph = graph.add_relation(relation)

        for frame in other.frames:
            graph = graph.add_frame(frame)

        merged_metadata = dict(graph.metadata)
        merged_metadata.update(other.metadata)

        return SemanticGraph(
            identifier=graph.identifier,
            concepts=graph.concepts,
            relations=graph.relations,
            frames=graph.frames,
            label=graph.label or other.label,
            description=graph.description or other.description,
            metadata=merged_metadata,
        )

    def __iter__(self) -> Iterator[SemanticConcept]:
        return iter(self.concepts)

    def __len__(self) -> int:
        return len(self.concepts)

    def __getitem__(self, index: int) -> SemanticConcept:
        return self.concepts[index]

    def __str__(self) -> str:
        return self.display_text
