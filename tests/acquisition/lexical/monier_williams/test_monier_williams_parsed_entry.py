
import pytest

from SanskritAI.acquisition.lexical.monier_williams import (
    MonierWilliamsParsedEntry,
)


def test_parsed_entry_stores_required_fields():
    entry = MonierWilliamsParsedEntry(
        headword="rāma",
        definition="pleasing; beautiful",
    )

    assert entry.headword == "rāma"
    assert entry.definition == "pleasing; beautiful"


def test_parsed_entry_stores_optional_fields():
    entry = MonierWilliamsParsedEntry(
        headword="rāma",
        definition="pleasing",
        grammatical_category="noun",
        transliteration="rāma",
        source_reference="MW",
    )

    assert entry.grammatical_category == "noun"
    assert entry.transliteration == "rāma"
    assert entry.source_reference == "MW"


def test_empty_headword_is_rejected():
    with pytest.raises(ValueError):
        MonierWilliamsParsedEntry(
            headword=" ",
            definition="meaning",
        )


def test_empty_definition_is_rejected():
    with pytest.raises(ValueError):
        MonierWilliamsParsedEntry(
            headword="rāma",
            definition=" ",
        )


def test_metadata_is_immutable():
    entry = MonierWilliamsParsedEntry(
        headword="rāma",
        definition="meaning",
        metadata={"source": "mw"},
    )

    with pytest.raises(TypeError):
        entry.metadata["source"] = "other"
