from SanskritAI.lexical.models.dictionary_entry_metadata import (
    DictionaryEntryMetadata,
)


def test_dictionary_entry_metadata_defaults():
    metadata = DictionaryEntryMetadata()
    assert metadata.dictionary_name == ""
    assert metadata.dictionary_version == ""
    assert metadata.entry_identifier == ""
    assert metadata.headword == ""


def test_dictionary_entry_metadata_stores_dictionary_information():
    metadata = DictionaryEntryMetadata(
        dictionary_name="Amarakośa",
        dictionary_version="1.0",
        entry_identifier="amara-001",
    )
    assert metadata.dictionary_name == "Amarakośa"
    assert metadata.dictionary_version == "1.0"
    assert metadata.entry_identifier == "amara-001"


def test_dictionary_entry_metadata_stores_headword():
    metadata = DictionaryEntryMetadata(
        headword="धर्म",
        transliteration="dharma",
    )
    assert metadata.headword == "धर्म"
    assert metadata.transliteration == "dharma"


def test_dictionary_entry_metadata_display_title_prefers_headword():
    metadata = DictionaryEntryMetadata(
        dictionary_name="Amarakośa",
        lemma="धर्म",
        headword="धर्म",
    )
    assert metadata.display_title == "धर्म"


def test_dictionary_entry_metadata_display_title_falls_back_to_lemma():
    metadata = DictionaryEntryMetadata(
        dictionary_name="Amarakośa",
        lemma="धर्म",
    )
    assert metadata.display_title == "धर्म"


def test_dictionary_entry_metadata_display_title_falls_back_to_dictionary():
    metadata = DictionaryEntryMetadata(
        dictionary_name="Amarakośa",
    )
    assert metadata.display_title == "Amarakośa"


def test_dictionary_entry_metadata_has_dictionary():
    metadata = DictionaryEntryMetadata(dictionary_name="Apte")
    assert metadata.has_dictionary is True


def test_dictionary_entry_metadata_has_headword():
    metadata = DictionaryEntryMetadata(headword="गज")
    assert metadata.has_headword is True


def test_dictionary_entry_metadata_has_location():
    metadata = DictionaryEntryMetadata(page="52")
    assert metadata.has_location is True


def test_dictionary_entry_metadata_has_no_location_by_default():
    metadata = DictionaryEntryMetadata()
    assert metadata.has_location is False


def test_dictionary_entry_metadata_citation_dictionary_only():
    metadata = DictionaryEntryMetadata(
        dictionary_name="Amarakośa",
    )
    assert metadata.citation == "Amarakośa"


def test_dictionary_entry_metadata_citation_with_volume_and_page():
    metadata = DictionaryEntryMetadata(
        dictionary_name="Amarakośa",
        volume="1",
        page="52",
    )
    assert metadata.citation == "Amarakośa Vol.1 p.52"


def test_dictionary_entry_metadata_is_immutable():
    metadata = DictionaryEntryMetadata(
        dictionary_name="Apte",
    )
    try:
        metadata.dictionary_name = "MW"
    except Exception:
        pass
    else:
        raise AssertionError("DictionaryEntryMetadata must be immutable.")
