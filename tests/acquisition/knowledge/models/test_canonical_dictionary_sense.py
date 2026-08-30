
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)


def test_dictionary_sense_creation():

    context = CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        chapter="12",
        verse="17",
    )

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams",
        short_name="MW",
        source_type="lexicon",
    )

    sense = CanonicalDictionarySense(
        sense_id="sense-001",
        entry_headword="राम",
        definition="A proper name.",
        gloss="Rama",
        semantic_notes="A personal name.",
        context=context,
        source=source,
        part_of_speech="noun",
        grammatical_gender="masculine",
        grammatical_number="singular",
        vibhakti="nominative",
        dhatu="√रम्",
        pratyaya="घञ्",
        samasa=None,
        sandhi=None,
        confidence=0.95,
    )

    assert sense.sense_id == "sense-001"
    assert sense.entry_headword == "राम"
    assert sense.definition == "A proper name."
    assert sense.gloss == "Rama"
    assert sense.context == context
    assert sense.source == source
    assert sense.part_of_speech == "noun"
    assert sense.vibhakti == "nominative"
    assert sense.confidence == 0.95


def test_has_context():

    context = CanonicalContext(
        corpus="Purāṇa",
    )

    sense = CanonicalDictionarySense(
        sense_id="s1",
        entry_headword="राम",
        definition="Rama",
        context=context,
    )

    assert sense.has_context is True


def test_has_context_false():

    sense = CanonicalDictionarySense(
        sense_id="s1",
        entry_headword="राम",
        definition="Rama",
    )

    assert sense.has_context is False


def test_has_source():

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    sense = CanonicalDictionarySense(
        sense_id="s1",
        entry_headword="राम",
        definition="Rama",
        source=source,
    )

    assert sense.has_source is True


def test_has_grammar():

    sense = CanonicalDictionarySense(
        sense_id="s1",
        entry_headword="राम",
        definition="Rama",
        part_of_speech="noun",
    )

    assert sense.has_grammar is True


def test_has_grammar_false():

    sense = CanonicalDictionarySense(
        sense_id="s1",
        entry_headword="राम",
        definition="Rama",
    )

    assert sense.has_grammar is False


def test_identifier():

    sense = CanonicalDictionarySense(
        sense_id="sense-001",
        entry_headword="राम",
        definition="Rama",
    )

    assert sense.identifier == "sense-001"


def test_summary():

    context = CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        chapter="12",
        verse="17",
    )

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams",
        short_name="MW",
    )

    sense = CanonicalDictionarySense(
        sense_id="s1",
        entry_headword="राम",
        definition="Rama",
        context=context,
        source=source,
        confidence=0.90,
    )

    assert sense.summary() == {
        "sense_id": "s1",
        "headword": "राम",
        "definition": "Rama",
        "context": context.identifier,
        "source": "MW",
        "confidence": 0.90,
    }


def test_sense_string_with_context():

    context = CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        chapter="12",
        verse="17",
    )

    sense = CanonicalDictionarySense(
        sense_id="s1",
        entry_headword="राम",
        definition="Rama",
        context=context,
    )

    assert (
        str(sense)
        == "CanonicalDictionarySense(राम @ Purāṇa:Śiva Purāṇa:12:17)"
    )


def test_sense_string_without_context():

    sense = CanonicalDictionarySense(
        sense_id="s1",
        entry_headword="राम",
        definition="Rama",
    )

    assert (
        str(sense)
        == "CanonicalDictionarySense(राम @ global)"
    )


def test_sense_immutability():

    sense = CanonicalDictionarySense(
        sense_id="s1",
        entry_headword="राम",
        definition="Rama",
    )

    with pytest.raises(Exception):
        sense.definition = "Hari"
