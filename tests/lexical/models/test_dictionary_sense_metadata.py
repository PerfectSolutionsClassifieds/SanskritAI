from SanskritAI.lexical.models.dictionary_sense_metadata import (
    DictionarySenseMetadata,
)


def test_dictionary_sense_metadata_defaults():
    metadata = DictionarySenseMetadata()
    assert metadata.sense_number == 1
    assert metadata.definition == ""
    assert metadata.short_definition == ""
    assert metadata.gloss == ""


def test_dictionary_sense_metadata_stores_meaning():
    metadata = DictionarySenseMetadata(
        sense_number=2,
        definition="A righteous way of life.",
        short_definition="righteousness",
        gloss="duty",
    )
    assert metadata.sense_number == 2
    assert metadata.definition == "A righteous way of life."
    assert metadata.short_definition == "righteousness"
    assert metadata.gloss == "duty"


def test_dictionary_sense_metadata_stores_classification():
    metadata = DictionarySenseMetadata(
        semantic_domain="ethics",
        usage_label="philosophical",
        register="formal",
    )
    assert metadata.semantic_domain == "ethics"
    assert metadata.usage_label == "philosophical"
    assert metadata.register == "formal"


def test_dictionary_sense_metadata_stores_linguistic_notes():
    metadata = DictionarySenseMetadata(
        grammatical_note="noun",
        etymology="Derived from dhṛ.",
    )
    assert metadata.grammatical_note == "noun"
    assert metadata.etymology == "Derived from dhṛ."


def test_dictionary_sense_metadata_examples_default_to_empty_list():
    metadata = DictionarySenseMetadata()
    assert metadata.examples == []


def test_dictionary_sense_metadata_citations_default_to_empty_list():
    metadata = DictionarySenseMetadata()
    assert metadata.citations == []


def test_dictionary_sense_metadata_cross_references_default_to_empty_list():
    metadata = DictionarySenseMetadata()
    assert metadata.cross_references == []


def test_dictionary_sense_metadata_stores_supporting_material():
    metadata = DictionarySenseMetadata(
        examples=["धर्मं चर"],
        citations=["Bhagavad Gītā 4.7"],
        cross_references=["sense-2"],
    )
    assert metadata.examples == ["धर्मं चर"]
    assert metadata.citations == ["Bhagavad Gītā 4.7"]
    assert metadata.cross_references == ["sense-2"]


def test_dictionary_sense_metadata_stores_notes():
    metadata = DictionarySenseMetadata(
        notes="Editorial note.",
    )
    assert metadata.notes == "Editorial note."


def test_dictionary_sense_metadata_inherits_lemma():
    metadata = DictionarySenseMetadata(
        lemma="धर्म",
    )
    assert metadata.lemma == "धर्म"
