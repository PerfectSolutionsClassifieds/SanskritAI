from SanskritAI.lexical.models.dictionary_entry import DictionaryEntry
from SanskritAI.lexical.models.dictionary_entry_metadata import (
    DictionaryEntryMetadata,
)
from SanskritAI.lexical.models.lexical_source import LexicalSource


def make_source():
    return LexicalSource(
        identifier="apte",
        name="Apte Sanskrit-English Dictionary",
    )


def make_metadata():
    return DictionaryEntryMetadata(
        dictionary_name="Apte",
        dictionary_version="1890",
        entry_identifier="apte-001",
        lemma="धर्म",
        headword="धर्म",
        transliteration="dharma",
        volume="1",
        page="421",
        entry_number="001",
        editor="V. S. Apte",
        publisher="Test Publisher",
        publication_year="1890",
        is_primary=True,
    )


def make_entry():
    return DictionaryEntry(
        identifier="entry-apte-dharma",
        metadata=make_metadata(),
        source=make_source(),
    )


def test_dictionary_entry_stores_identifier():
    assert make_entry().identifier == "entry-apte-dharma"


def test_dictionary_entry_exposes_source():
    entry = make_entry()
    assert entry.source is not None
    assert entry.source.identifier == "apte"


def test_dictionary_entry_exposes_source_name():
    assert make_entry().source_name == "Apte Sanskrit-English Dictionary"


def test_dictionary_entry_exposes_source_identifier():
    assert make_entry().source_identifier == "apte"


def test_dictionary_entry_exposes_dictionary_name():
    assert make_entry().dictionary_name == "Apte"


def test_dictionary_entry_exposes_dictionary_version():
    assert make_entry().dictionary_version == "1890"


def test_dictionary_entry_exposes_entry_identifier():
    assert make_entry().entry_identifier == "apte-001"


def test_dictionary_entry_exposes_headword():
    assert make_entry().headword == "धर्म"


def test_dictionary_entry_exposes_transliteration():
    assert make_entry().transliteration == "dharma"


def test_dictionary_entry_exposes_volume():
    assert make_entry().volume == "1"


def test_dictionary_entry_exposes_page():
    assert make_entry().page == "421"


def test_dictionary_entry_exposes_entry_number():
    assert make_entry().entry_number == "001"


def test_dictionary_entry_exposes_editor():
    assert make_entry().editor == "V. S. Apte"


def test_dictionary_entry_exposes_publisher():
    assert make_entry().publisher == "Test Publisher"


def test_dictionary_entry_exposes_publication_year():
    assert make_entry().publication_year == "1890"


def test_dictionary_entry_exposes_primary_status():
    assert make_entry().is_primary is True


def test_dictionary_entry_exposes_citation():
    assert make_entry().citation == "Apte Vol.1 p.421"


def test_dictionary_entry_exposes_display_title():
    assert make_entry().display_title == "धर्म"
