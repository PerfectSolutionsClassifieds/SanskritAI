
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


def make_sense(
    sense_id,
    headword="राम",
    definition="Rama",
):

    return CanonicalDictionarySense(
        sense_id=sense_id,
        entry_headword=headword,
        definition=definition,
    )


def test_dictionary_entry_creation():

    sense = make_sense(
        "s1",
        definition="Rama",
    )

    entry = CanonicalDictionaryEntry(
        headword="राम",
        transliteration="rāma",
        lemma="राम",
        senses=(sense,),
        source_name="Monier-Williams",
        source_version="1.0",
        source_record_id="MW-001",
    )

    assert entry.headword == "राम"
    assert entry.transliteration == "rāma"
    assert entry.lemma == "राम"
    assert entry.sense_count == 1
    assert entry.source_name == "Monier-Williams"


def test_sense_count():

    senses = (
        make_sense("s1"),
        make_sense("s2"),
        make_sense("s3"),
    )

    entry = CanonicalDictionaryEntry(
        headword="राम",
        senses=senses,
    )

    assert entry.sense_count == 3
    assert len(entry) == 3


def test_display_name():

    entry = CanonicalDictionaryEntry(
        headword="राम",
    )

    assert entry.display_name == "राम"


def test_has_transliteration():

    entry = CanonicalDictionaryEntry(
        headword="राम",
        transliteration="rāma",
    )

    assert entry.has_transliteration is True


def test_has_transliteration_false():

    entry = CanonicalDictionaryEntry(
        headword="राम",
    )

    assert entry.has_transliteration is False


def test_has_multiple_senses():

    entry = CanonicalDictionaryEntry(
        headword="राम",
        senses=(
            make_sense("s1"),
            make_sense("s2"),
        ),
    )

    assert entry.has_multiple_senses is True


def test_has_multiple_senses_false():

    entry = CanonicalDictionaryEntry(
        headword="राम",
        senses=(make_sense("s1"),),
    )

    assert entry.has_multiple_senses is False


def test_primary_sense():

    first = make_sense("s1")
    second = make_sense("s2")

    entry = CanonicalDictionaryEntry(
        headword="राम",
        senses=(first, second),
    )

    assert entry.primary_sense() == first


def test_primary_sense_empty():

    entry = CanonicalDictionaryEntry(
        headword="राम",
    )

    assert entry.primary_sense() is None


def test_summary():

    entry = CanonicalDictionaryEntry(
        headword="राम",
        lemma="राम",
        source_name="MW",
        entry_type="noun",
        senses=(
            make_sense("s1"),
            make_sense("s2"),
        ),
    )

    assert entry.summary() == {
        "headword": "राम",
        "lemma": "राम",
        "source": "MW",
        "entry_type": "noun",
        "sense_count": 2,
    }


def test_iteration():

    first = make_sense("s1")
    second = make_sense("s2")

    entry = CanonicalDictionaryEntry(
        headword="राम",
        senses=(first, second),
    )

    assert list(entry) == [first, second]


def test_string():

    entry = CanonicalDictionaryEntry(
        headword="राम",
        senses=(
            make_sense("s1"),
            make_sense("s2"),
        ),
    )

    assert (
        str(entry)
        == "CanonicalDictionaryEntry(राम, 2 senses)"
    )


def test_entry_immutability():

    entry = CanonicalDictionaryEntry(
        headword="राम",
    )

    with pytest.raises(Exception):
        entry.headword = "हरि"
