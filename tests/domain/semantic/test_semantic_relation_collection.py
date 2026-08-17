from __future__ import annotations

from SanskritAI.domain.semantic.semantic_concept import (
    SemanticConcept,
)
from SanskritAI.domain.semantic.semantic_relation import (
    SemanticRelation,
)
from SanskritAI.domain.semantic.semantic_relation_collection import (
    SemanticRelationCollection,
)


def make_relation(
    identifier: str,
    relation: str = "means",
) -> SemanticRelation:
    source = SemanticConcept(
        identifier=f"{identifier}-source",
        name="source",
    )

    target = SemanticConcept(
        identifier=f"{identifier}-target",
        name="target",
    )

    return SemanticRelation(
        identifier=identifier,
        relation=relation,
        source=source,
        target=target,
    )


class TestSemanticRelationCollection:
    def test_can_be_created_empty(self):
        collection = SemanticRelationCollection()

        assert collection is not None

    def test_empty_collection_has_zero_count(self):
        collection = SemanticRelationCollection()

        assert collection.count == 0
        assert len(collection) == 0

    def test_empty_collection_is_empty(self):
        collection = SemanticRelationCollection()

        assert collection.is_empty is True

    def test_empty_collection_has_no_first_relation(self):
        collection = SemanticRelationCollection()

        assert collection.first is None

    def test_accepts_relations_as_tuple(self):
        first = make_relation("r1")
        second = make_relation("r2")

        collection = SemanticRelationCollection(
            relations=(first, second)
        )

        assert collection.relations == (first, second)

    def test_count_matches_number_of_relations(self):
        first = make_relation("r1")
        second = make_relation("r2")

        collection = SemanticRelationCollection(
            relations=(first, second)
        )

        assert collection.count == 2
        assert len(collection) == 2

    def test_first_returns_first_relation(self):
        first = make_relation("r1")
        second = make_relation("r2")

        collection = SemanticRelationCollection(
            relations=(first, second)
        )

        assert collection.first is first

    def test_is_immutable_at_collection_level(self):
        relation = make_relation("r1")

        collection = SemanticRelationCollection(
            relations=(relation,)
        )

        try:
            collection.relations = ()
        except (AttributeError, TypeError):
            pass
        else:
            raise AssertionError(
                "SemanticRelationCollection must be immutable."
            )

    def test_add_returns_new_collection(self):
        first = make_relation("r1")
        second = make_relation("r2")

        original = SemanticRelationCollection(
            relations=(first,)
        )

        updated = original.add(second)

        assert original.relations == (first,)
        assert updated.relations == (first, second)

    def test_extend_returns_new_collection(self):
        first = make_relation("r1")
        second = make_relation("r2")

        left = SemanticRelationCollection(
            relations=(first,)
        )

        right = SemanticRelationCollection(
            relations=(second,)
        )

        combined = left.extend(right)

        assert left.relations == (first,)
        assert right.relations == (second,)
        assert combined.relations == (first, second)

    def test_iteration(self):
        first = make_relation("r1")
        second = make_relation("r2")

        collection = SemanticRelationCollection(
            relations=(first, second)
        )

        assert tuple(collection) == (first, second)

    def test_indexing(self):
        first = make_relation("r1")
        second = make_relation("r2")

        collection = SemanticRelationCollection(
            relations=(first, second)
        )

        assert collection[0] is first
        assert collection[1] is second

    def test_display_name(self):
        collection = SemanticRelationCollection()

        assert collection.display_name == "Semantic Relations"

    def test_display_text(self):
        collection = SemanticRelationCollection()

        assert collection.display_text == "0 relations"

    def test_display_description(self):
        collection = SemanticRelationCollection()

        assert (
            collection.display_description
            == "Immutable collection of semantic relations."
        )

    def test_string_representation(self):
        collection = SemanticRelationCollection()

        assert str(collection) == "0 relations"
