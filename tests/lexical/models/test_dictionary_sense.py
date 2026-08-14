from SanskritAI.lexical.models.dictionary_sense import DictionarySense
from SanskritAI.lexical.models.dictionary_sense_metadata import (
    DictionarySenseMetadata,
)


def make_metadata():
    return DictionarySenseMetadata(
        lemma="धर्म",
        sense_number=2,
        definition="Righteousness or duty.",
        short_definition="duty",
        gloss="dharma",
        semantic_domain="ethics",
        usage_label="philosophical",
        register="formal",
        grammatical_note="noun",
        etymology="From धृ.",
        examples=["धर्मं चर"],
        citations=["Bhagavad Gītā"],
        cross_references=["sense-1"],
        notes="Editorial note.",
    )


def make_sense():
    return DictionarySense(
        identifier="sense-dharma-2",
        metadata=make_metadata(),
    )


def test_dictionary_sense_stores_identifier():
    assert make_sense().identifier == "sense-dharma-2"


def test_dictionary_sense_exposes_sense_number():
    assert make_sense().sense_number == 2


def test_dictionary_sense_exposes_definition():
    assert make_sense().definition == "Righteousness or duty."


def test_dictionary_sense_exposes_short_definition():
    assert make_sense().short_definition == "duty"


def test_dictionary_sense_exposes_gloss():
    assert make_sense().gloss == "dharma"


def test_dictionary_sense_exposes_semantic_domain():
    assert make_sense().semantic_domain == "ethics"


def test_dictionary_sense_exposes_usage_label():
    assert make_sense().usage_label == "philosophical"


def test_dictionary_sense_exposes_register():
    assert make_sense().register == "formal"


def test_dictionary_sense_exposes_grammatical_note():
    assert make_sense().grammatical_note == "noun"


def test_dictionary_sense_exposes_etymology():
    assert make_sense().etymology == "From धृ."


def test_dictionary_sense_exposes_examples():
    assert make_sense().examples == ["धर्मं चर"]


def test_dictionary_sense_exposes_citations():
    assert make_sense().citations == ["Bhagavad Gītā"]


def test_dictionary_sense_exposes_cross_references():
    assert make_sense().cross_references == ["sense-1"]


def test_dictionary_sense_is_a_leaf_node():
    sense = make_sense()
    assert not hasattr(sense, "children") or sense.children == []
