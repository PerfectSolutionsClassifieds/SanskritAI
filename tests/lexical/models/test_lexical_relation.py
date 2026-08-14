from SanskritAI.lexical.models.lexical_relation import LexicalRelation
from SanskritAI.lexical.models.lexical_relation_metadata import (
    LexicalRelationMetadata,
)
from SanskritAI.lexical.enums.relation_type import RelationType


def make_metadata():
    return LexicalRelationMetadata(
        relation_type=RelationType.RELATED,
        source_identifier="lexeme-dharma",
        target_identifier="lexeme-rta",
        directed=True,
        weight=0.8,
        confidence=0.95,
        source_dictionary="Amarakośa",
        notes="Lexical relationship.",
    )


def make_relation():
    return LexicalRelation(
        identifier="relation-001",
        metadata=make_metadata(),
    )


def test_lexical_relation_stores_identifier():
    assert make_relation().identifier == "relation-001"


def test_lexical_relation_exposes_relation_type():
    assert make_relation().relation_type == RelationType.RELATED


def test_lexical_relation_exposes_source_identifier():
    assert make_relation().source_identifier == "lexeme-dharma"


def test_lexical_relation_exposes_target_identifier():
    assert make_relation().target_identifier == "lexeme-rta"


def test_lexical_relation_exposes_directed():
    assert make_relation().directed is True


def test_lexical_relation_exposes_weight():
    assert make_relation().weight == 0.8


def test_lexical_relation_exposes_confidence():
    assert make_relation().confidence == 0.95


def test_lexical_relation_exposes_source_dictionary():
    assert make_relation().source_dictionary == "Amarakośa"


def test_lexical_relation_preserves_metadata():
    relation = make_relation()
    assert relation.metadata == make_metadata()


def test_lexical_relation_can_be_undirected():
    metadata = LexicalRelationMetadata(
        relation_type=RelationType.RELATED,
        source_identifier="a",
        target_identifier="b",
        directed=False,
    )
    relation = LexicalRelation(
        identifier="relation-undirected",
        metadata=metadata,
    )
    assert relation.directed is False


def test_lexical_relation_default_weight():
    metadata = LexicalRelationMetadata()
    assert metadata.weight == 1.0


def test_lexical_relation_default_confidence():
    metadata = LexicalRelationMetadata()
    assert metadata.confidence == 1.0
