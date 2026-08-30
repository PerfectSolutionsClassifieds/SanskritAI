
from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)


# =========================================================
# Construction
# =========================================================

def test_canonical_lexicon_minimal_construction():
    lexicon = CanonicalLexicon(
        identifier="test.lexicon",
        name="Test Lexicon",
        version="1.0",
    )

    assert lexicon.identifier == "test.lexicon"
    assert lexicon.name == "Test Lexicon"
    assert lexicon.version == "1.0"
    assert lexicon.language == "sa"
    assert lexicon.description is None
    assert lexicon.source is None
    assert lexicon.entries == {}


def test_canonical_lexicon_full_construction():
    lexicon = CanonicalLexicon(
        identifier="mw.test",
        name="Monier-Williams Test",
        version="1.0.0",
        language="sa",
        description="Test canonical lexicon",
        source="Monier-Williams",
        entries={},
    )

    assert lexicon.identifier == "mw.test"
    assert lexicon.name == "Monier-Williams Test"
    assert lexicon.version == "1.0.0"
    assert lexicon.language == "sa"
    assert lexicon.description == "Test canonical lexicon"
    assert lexicon.source == "Monier-Williams"


# =========================================================
# Empty lexicon
# =========================================================

def test_empty_lexicon_entry_count():
    lexicon = CanonicalLexicon(
        identifier="empty",
        name="Empty Lexicon",
        version="1.0",
    )

    assert lexicon.entry_count == 0
    assert len(lexicon) == 0


def test_empty_lexicon_sense_count():
    lexicon = CanonicalLexicon(
        identifier="empty",
        name="Empty Lexicon",
        version="1.0",
    )

    assert lexicon.sense_count == 0


def test_empty_lexicon_all_entries():
    lexicon = CanonicalLexicon(
        identifier="empty",
        name="Empty Lexicon",
        version="1.0",
    )

    assert lexicon.all_entries() == ()


def test_empty_lexicon_all_senses():
    lexicon = CanonicalLexicon(
        identifier="empty",
        name="Empty Lexicon",
        version="1.0",
    )

    assert tuple(lexicon.all_senses()) == ()


def test_empty_lexicon_all_contexts():
    lexicon = CanonicalLexicon(
        identifier="empty",
        name="Empty Lexicon",
        version="1.0",
    )

    assert tuple(lexicon.all_contexts()) == ()


def test_empty_lexicon_all_sources():
    lexicon = CanonicalLexicon(
        identifier="empty",
        name="Empty Lexicon",
        version="1.0",
    )

    assert tuple(lexicon.all_sources()) == ()


# =========================================================
# Test graph builders
# =========================================================

def make_context():
    return CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        section="Rudra Saṁhitā",
        chapter="12",
        verse="17",
    )


def make_source():
    return CanonicalSource(
        source_id="shiva-purana",
        name="Śiva Purāṇa",
        short_name="SP",
        source_type="primary_text",
    )


def make_sense(
    sense_id,
    context=None,
    source=None,
):
    return CanonicalDictionarySense(
        sense_id=sense_id,
        entry_headword="शिव",
        definition="auspicious",
        context=context,
        source=source,
    )


def make_entry(
    headword,
    senses=(),
):
    return CanonicalDictionaryEntry(
        headword=headword,
        transliteration=None,
        senses=tuple(senses),
        source_name="Test Dictionary",
        source_version="1.0",
        source_record_id=headword,
    )


# =========================================================
# Entry operations
# =========================================================

def test_lexicon_entry_count():
    entry1 = make_entry("शिव")
    entry2 = make_entry("हरि")

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry1,
            "हरि": entry2,
        },
    )

    assert lexicon.entry_count == 2
    assert len(lexicon) == 2


def test_lexicon_contains():
    entry = make_entry("शिव")

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry,
        },
    )

    assert lexicon.contains("शिव")
    assert not lexicon.contains("हरि")


def test_lexicon_get_existing_entry():
    entry = make_entry("शिव")

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry,
        },
    )

    assert lexicon.get("शिव") is entry


def test_lexicon_get_missing_entry():
    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
    )

    assert lexicon.get("अज्ञात") is None


def test_lexicon_all_entries():
    entry1 = make_entry("शिव")
    entry2 = make_entry("हरि")

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry1,
            "हरि": entry2,
        },
    )

    entries = lexicon.all_entries()

    assert isinstance(entries, tuple)
    assert entries == (entry1, entry2)


def test_lexicon_iteration():
    entry1 = make_entry("शिव")
    entry2 = make_entry("हरि")

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry1,
            "हरि": entry2,
        },
    )

    assert tuple(iter(lexicon)) == (
        entry1,
        entry2,
    )


# =========================================================
# Sense traversal
# =========================================================

def test_lexicon_sense_count():
    sense1 = make_sense("s1")
    sense2 = make_sense("s2")
    sense3 = make_sense("s3")

    entry1 = make_entry(
        "शिव",
        senses=(sense1, sense2),
    )

    entry2 = make_entry(
        "हरि",
        senses=(sense3,),
    )

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry1,
            "हरि": entry2,
        },
    )

    assert lexicon.sense_count == 3


def test_lexicon_all_senses():
    sense1 = make_sense("s1")
    sense2 = make_sense("s2")
    sense3 = make_sense("s3")

    entry1 = make_entry(
        "शिव",
        senses=(sense1, sense2),
    )

    entry2 = make_entry(
        "हरि",
        senses=(sense3,),
    )

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry1,
            "हरि": entry2,
        },
    )

    assert tuple(lexicon.all_senses()) == (
        sense1,
        sense2,
        sense3,
    )


# =========================================================
# Context traversal
# =========================================================

def test_lexicon_all_contexts_deduplicates_contexts():
    context = make_context()

    sense1 = make_sense(
        "s1",
        context=context,
    )

    sense2 = make_sense(
        "s2",
        context=context,
    )

    entry = make_entry(
        "शिव",
        senses=(sense1, sense2),
    )

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry,
        },
    )

    contexts = tuple(lexicon.all_contexts())

    assert contexts == (context,)


def test_lexicon_all_contexts_ignores_missing_context():
    context = make_context()

    sense1 = make_sense(
        "s1",
        context=None,
    )

    sense2 = make_sense(
        "s2",
        context=context,
    )

    entry = make_entry(
        "शिव",
        senses=(sense1, sense2),
    )

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry,
        },
    )

    assert tuple(lexicon.all_contexts()) == (context,)


# =========================================================
# Source traversal
# =========================================================

def test_lexicon_all_sources_deduplicates_sources():
    source = make_source()

    sense1 = make_sense(
        "s1",
        source=source,
    )

    sense2 = make_sense(
        "s2",
        source=source,
    )

    entry = make_entry(
        "शिव",
        senses=(sense1, sense2),
    )

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry,
        },
    )

    sources = tuple(lexicon.all_sources())

    assert sources == (source,)


def test_lexicon_all_sources_ignores_missing_source():
    source = make_source()

    sense1 = make_sense(
        "s1",
        source=None,
    )

    sense2 = make_sense(
        "s2",
        source=source,
    )

    entry = make_entry(
        "शिव",
        senses=(sense1, sense2),
    )

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
        entries={
            "शिव": entry,
        },
    )

    assert tuple(lexicon.all_sources()) == (source,)


# =========================================================
# Summary
# =========================================================

def test_lexicon_summary():
    sense1 = make_sense("s1")
    sense2 = make_sense("s2")

    entry = make_entry(
        "शिव",
        senses=(sense1, sense2),
    )

    lexicon = CanonicalLexicon(
        identifier="test.lexicon",
        name="Test Lexicon",
        version="1.0",
        entries={
            "शिव": entry,
        },
    )

    assert lexicon.summary() == {
        "identifier": "test.lexicon",
        "name": "Test Lexicon",
        "version": "1.0",
        "entries": 1,
        "senses": 2,
    }


# =========================================================
# String representation
# =========================================================

def test_lexicon_string_representation():
    sense = make_sense("s1")
    entry = make_entry(
        "शिव",
        senses=(sense,),
    )

    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test Lexicon",
        version="1.0",
        entries={
            "शिव": entry,
        },
    )

    assert str(lexicon) == (
        "CanonicalLexicon("
        "Test Lexicon, "
        "1 entries, "
        "1 senses)"
    )


# =========================================================
# Immutability
# =========================================================

def test_canonical_lexicon_is_frozen():
    lexicon = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
    )

    try:
        lexicon.name = "Changed"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "CanonicalLexicon should be immutable"
        )


# =========================================================
# Equality
# =========================================================

def test_canonical_lexicon_equality():
    lexicon1 = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
    )

    lexicon2 = CanonicalLexicon(
        identifier="test",
        name="Test",
        version="1.0",
    )

    assert lexicon1 == lexicon2
