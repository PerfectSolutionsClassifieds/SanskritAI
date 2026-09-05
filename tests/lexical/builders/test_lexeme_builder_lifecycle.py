from SanskritAI.lexical.builders.lexeme_builder import (
    LexemeBuilder,
)


def test_lexeme_builder_has_initial_instance():
    builder = LexemeBuilder()

    instance = builder.instance()

    assert instance.identifier == ""
    assert instance.lemma == ""


def test_lexeme_builder_instance_tracks_fluent_state():
    builder = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
        .with_transliteration("dharma")
    )

    instance = builder.instance()

    assert instance.identifier == "lex-001"
    assert instance.lemma == "धर्म"
    assert instance.transliteration == "dharma"


def test_lexeme_builder_build_returns_current_instance():
    builder = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
    )

    built = builder.build()

    assert built.identifier == "lex-001"
    assert built.lemma == "धर्म"


def test_lexeme_builder_reset_restores_default_state():
    builder = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
    )

    builder.reset()

    instance = builder.instance()

    assert instance.identifier == ""
    assert instance.lemma == ""


def test_lexeme_builder_clone_preserves_state():
    builder = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
    )

    clone = builder.clone()

    assert clone.instance() == builder.instance()
    assert clone is not builder


def test_lexeme_builder_from_instance_restores_state():
    source = (
        LexemeBuilder()
        .with_identifier("lex-001")
        .with_lemma("धर्म")
    )

    instance = source.build()

    restored = LexemeBuilder().from_instance(instance)

    assert restored.instance() == instance
    assert restored.build() == instance
