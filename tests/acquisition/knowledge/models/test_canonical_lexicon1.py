
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)


def make_sense(
    sense_id,
    headword,
    context=None,
    source=None,
):

    return CanonicalDictionarySense(
        sense_id=sense_id,
        entry_headword=headword,
        definition=f"Definition of {headword}",
        context=context,
        source=source,
    )


def make_entry(
    headword,
    senses=(),
):

    return CanonicalDictionaryEntry(
        headword=headword,
        lemma=headword,
        senses=senses,
    )


def test_empty_lexicon():

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test Lexicon",
        version="1.0",
    )

    assert lexicon.entry_count == 0
    assert lexicon.sense_count == 0
    assert len(lexicon) == 0
    assert lexicon.all_entries() == ()


def test_lexicon_creation():

    entry = make_entry(
        "राम",
        senses=(
            make_sense("s1", "राम"),
        ),
    )

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test Lexicon",
        version="1.0",
        entries={
            "राम": entry,
        },
    )

    assert lexicon.identifier == "lexicon-001"
    assert lexicon.name == "Test Lexicon"
    assert lexicon.version == "1.0"
    assert lexicon.entry_count == 1
    assert lexicon.sense_count == 1


def test_contains():

    entry = make_entry("राम")

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
        entries={"राम": entry},
    )

    assert lexicon.contains("राम") is True
    assert lexicon.contains("हरि") is False


def test_get():

    entry = make_entry("राम")

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
        entries={"राम": entry},
    )

    assert lexicon.get("राम") == entry
    assert lexicon.get("हरि") is None


def test_all_entries():

    first = make_entry("राम")
    second = make_entry("हरि")

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
        entries={
            "राम": first,
            "हरि": second,
        },
    )

    assert lexicon.all_entries() == (
        first,
        second,
    )


def test_all_senses():

    first = make_sense("s1", "राम")
    second = make_sense("s2", "राम")
    third = make_sense("s3", "हरि")

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
        entries={
            "राम": make_entry(
                "राम",
                senses=(first, second),
            ),
            "हरि": make_entry(
                "हरि",
                senses=(third,),
            ),
        },
    )

    assert tuple(lexicon.all_senses()) == (
        first,
        second,
        third,
    )


def test_all_contexts_deduplicates_contexts():

    context = CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        chapter="12",
        verse="17",
    )

    first = make_sense(
        "s1",
        "राम",
        context=context,
    )

    second = make_sense(
        "s2",
        "हरि",
        context=context,
    )

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
        entries={
            "राम": make_entry(
                "राम",
                senses=(first,),
            ),
            "हरि": make_entry(
                "हरि",
                senses=(second,),
            ),
        },
    )

    contexts = tuple(
        lexicon.all_contexts()
    )

    assert contexts == (context,)


def test_all_sources_deduplicates_sources():

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams",
        short_name="MW",
    )

    first = make_sense(
        "s1",
        "राम",
        source=source,
    )

    second = make_sense(
        "s2",
        "हरि",
        source=source,
    )

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
        entries={
            "राम": make_entry(
                "राम",
                senses=(first,),
            ),
            "हरि": make_entry(
                "हरि",
                senses=(second,),
            ),
        },
    )

    sources = tuple(
        lexicon.all_sources()
    )

    assert sources == (source,)


def test_sense_count_across_entries():

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
        entries={
            "राम": make_entry(
                "राम",
                senses=(
                    make_sense("s1", "राम"),
                    make_sense("s2", "राम"),
                ),
            ),
            "हरि": make_entry(
                "हरि",
                senses=(
                    make_sense("s3", "हरि"),
                ),
            ),
        },
    )

    assert lexicon.entry_count == 2
    assert lexicon.sense_count == 3


def test_lexicon_summary():

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test Lexicon",
        version="1.0",
        entries={
            "राम": make_entry(
                "राम",
                senses=(
                    make_sense("s1", "राम"),
                ),
            ),
            "हरि": make_entry(
                "हरि",
                senses=(
                    make_sense("s2", "हरि"),
                    make_sense("s3", "हरि"),
                ),
            ),
        },
    )

    assert lexicon.summary() == {
        "identifier": "lexicon-001",
        "name": "Test Lexicon",
        "version": "1.0",
        "entries": 2,
        "senses": 3,
    }


def test_lexicon_iteration():

    first = make_entry("राम")
    second = make_entry("हरि")

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
        entries={
            "राम": first,
            "हरि": second,
        },
    )

    assert list(lexicon) == [
        first,
        second,
    ]


def test_lexicon_string():

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
        entries={
            "राम": make_entry(
                "राम",
                senses=(
                    make_sense("s1", "राम"),
                    make_sense("s2", "राम"),
                ),
            ),
        },
    )

    assert (
        str(lexicon)
        == "CanonicalLexicon(Test, 1 entries, 2 senses)"
    )


def test_lexicon_immutability():

    lexicon = CanonicalLexicon(
        identifier="lexicon-001",
        name="Test",
        version="1.0",
    )

    with pytest.raises(Exception):
        lexicon.name = "Changed"
