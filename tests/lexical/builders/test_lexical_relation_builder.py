from SanskritAI.lexical.builders.lexical_relation_builder import (
    LexicalRelationBuilder,
)
from SanskritAI.lexical.enums.relation_type import RelationType


def test_lexical_relation_builder_builds_relation():
    relation = (
        LexicalRelationBuilder()
        .with_identifier("rel-001")
        .with_relation_type(RelationType.SYNONYM)
        .between("lex-001", "lex-002")
        .build()
    )

    assert relation.identifier == "rel-001"
    assert relation.metadata.relation_type == RelationType.SYNONYM
    assert relation.metadata.source_identifier == "lex-001"
    assert relation.metadata.target_identifier == "lex-002"


def test_lexical_relation_builder_supports_weight_and_confidence():
    relation = (
        LexicalRelationBuilder()
        .with_identifier("rel-001")
        .between("lex-001", "lex-002")
        .with_weight(0.75)
        .with_confidence(0.95)
        .build()
    )

    assert relation.metadata.weight == 0.75
    assert relation.metadata.confidence == 0.95


def test_lexical_relation_builder_supports_directed():
    relation = (
        LexicalRelationBuilder()
        .with_identifier("rel-001")
        .between("lex-001", "lex-002")
        .directed(False)
        .build()
    )

    assert relation.metadata.directed is False


def test_lexical_relation_builder_has_instance():
    builder = (
        LexicalRelationBuilder()
        .with_identifier("rel-001")
        .between("lex-001", "lex-002")
    )

    instance = builder.instance()

    assert instance.identifier == "rel-001"
    assert instance.metadata.source_identifier == "lex-001"
    assert instance.metadata.target_identifier == "lex-002"


def test_lexical_relation_builder_reset():
    builder = (
        LexicalRelationBuilder()
        .with_identifier("rel-001")
        .between("lex-001", "lex-002")
    )

    builder.reset()

    relation = builder.instance()

    assert relation.identifier == ""
    assert relation.metadata.source_identifier == ""
    assert relation.metadata.target_identifier == ""


def test_lexical_relation_builder_clone():
    builder = (
        LexicalRelationBuilder()
        .with_identifier("rel-001")
        .between("lex-001", "lex-002")
    )

    clone = builder.clone()

    assert clone.instance() == builder.instance()
    assert clone is not builder
