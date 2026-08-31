
from __future__ import annotations

from SanskritAI.acquisition.knowledge.builders.canonical_index_builder import (
    CanonicalIndexBuilder,
)

from SanskritAI.acquisition.knowledge.indexes.headword_index import (
    HeadwordIndex,
)

from SanskritAI.acquisition.knowledge.indexes.lemma_index import (
    LemmaIndex,
)

from SanskritAI.acquisition.knowledge.indexes.context_index import (
    ContextIndex,
)

from SanskritAI.acquisition.knowledge.indexes.source_index import (
    SourceIndex,
)

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

from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)


# =========================================================
# Helpers
# =========================================================


def make_lemma(
    text: str = "राम",
) -> CanonicalLemma:
    """
    Creates a CanonicalLemma using the current model contract.
    """

    return CanonicalLemma(
        lemma=text,
    )


def make_context(
    identifier: str = "context-1",
) -> CanonicalContext:
    """
    Creates a CanonicalContext.

    The current ContextIndex API exposes the canonical
    context identifier through ``context.identifier``.
    """

    return CanonicalContext(
        context_id=identifier,
    )


def make_source(
    source_id: str = "source-1",
) -> CanonicalSource:
    """
    Creates a CanonicalSource.
    """

    return CanonicalSource(
        source_id=source_id,
        name=source_id,
    )


def make_sense(
    context: CanonicalContext | None = None,
    source: CanonicalSource | None = None,
    sense_id: str = "sense-1",
    entry_headword: str = "राम",
    definition: str = "a name or person",
) -> CanonicalDictionarySense:
    """
    Creates a canonical dictionary sense using the current
    required constructor fields.
    """

    return CanonicalDictionarySense(
        sense_id=sense_id,
        entry_headword=entry_headword,
        definition=definition,
        context=context,
        source=source,
    )


def make_entry(
    headword: str = "राम",
    lemma: CanonicalLemma | None = None,
    senses: tuple[CanonicalDictionarySense, ...] = (),
) -> CanonicalDictionaryEntry:
    """
    Creates a canonical dictionary entry.
    """

    entry = CanonicalDictionaryEntry(
        headword=headword,
        lemma=lemma,
    )

    for sense in senses:
        entry.add_sense(
            sense,
        )

    return entry


def make_lexicon(
    *entries: CanonicalDictionaryEntry,
) -> CanonicalLexicon:
    """
    Creates a canonical lexicon using its required identity
    fields.
    """

    lexicon = CanonicalLexicon(
        identifier="test-lexicon",
        name="Test Lexicon",
        version="1.0",
    )

    for entry in entries:
        lexicon.add(
            entry,
        )

    return lexicon


def make_builder() -> CanonicalIndexBuilder:
    """
    Creates a fully initialized CanonicalIndexBuilder.
    """

    return CanonicalIndexBuilder(
        headword_index=HeadwordIndex(),
        lemma_index=LemmaIndex(),
        context_index=ContextIndex(),
        source_index=SourceIndex(),
    )


# =========================================================
# Construction
# =========================================================


def test_builder_can_be_constructed():
    builder = make_builder()

    assert isinstance(
        builder,
        CanonicalIndexBuilder,
    )


def test_builder_contains_all_four_indexes():
    builder = make_builder()

    assert isinstance(
        builder.headword_index,
        HeadwordIndex,
    )

    assert isinstance(
        builder.lemma_index,
        LemmaIndex,
    )

    assert isinstance(
        builder.context_index,
        ContextIndex,
    )

    assert isinstance(
        builder.source_index,
        SourceIndex,
    )


# =========================================================
# Empty Build
# =========================================================


def test_build_empty_lexicon_collection_clears_indexes():
    builder = make_builder()

    builder.build(
        (),
    )

    assert len(builder.headword_index) == 0
    assert len(builder.lemma_index) == 0
    assert len(builder.context_index) == 0
    assert len(builder.source_index) == 0


# =========================================================
# Headword Index
# =========================================================


def test_build_indexes_dictionary_entry_headword():
    lemma = make_lemma()

    entry = make_entry(
        "राम",
        lemma=lemma,
    )

    lexicon = make_lexicon(
        entry,
    )

    builder = make_builder()

    builder.build(
        (lexicon,),
    )

    assert (
        builder.headword_index.lookup("राम")
        is entry
    )


def test_build_indexes_multiple_headwords():
    first = make_entry(
        "राम",
        lemma=make_lemma("राम"),
    )

    second = make_entry(
        "हरि",
        lemma=make_lemma("हरि"),
    )

    lexicon = make_lexicon(
        first,
        second,
    )

    builder = make_builder()

    builder.build(
        (lexicon,),
    )

    assert (
        builder.headword_index.lookup("राम")
        is first
    )

    assert (
        builder.headword_index.lookup("हरि")
        is second
    )


# =========================================================
# Lemma Index
# =========================================================


def test_build_indexes_entry_lemma():
    lemma = make_lemma(
        "राम",
    )

    entry = make_entry(
        "रामः",
        lemma=lemma,
    )

    lexicon = make_lexicon(
        entry,
    )

    builder = make_builder()

    builder.build(
        (lexicon,),
    )

    assert (
        builder.lemma_index.lookup("राम")
        is lemma
    )

    assert (
        builder.lemma_index.lookup_text("राम")
        is lemma
    )


def test_entry_without_lemma_is_not_added_to_lemma_index():
    entry = make_entry(
        "रामः",
        lemma=None,
    )

    lexicon = make_lexicon(
        entry,
    )

    builder = make_builder()

    builder.build(
        (lexicon,),
    )

    assert len(builder.lemma_index) == 0


# =========================================================
# Context Index
# =========================================================


def test_build_indexes_sense_context():
    context = make_context(
        "ramayana.chapter.1",
    )

    sense = make_sense(
        context=context,
    )

    entry = make_entry(
        "राम",
        senses=(sense,),
    )

    lexicon = make_lexicon(
        entry,
    )

    builder = make_builder()

    builder.build(
        (lexicon,),
    )

    assert (
        sense
        in builder.context_index.lookup(
            "ramayana.chapter.1",
        )
    )


def test_sense_without_context_is_not_added_to_context_index():
    sense = make_sense(
        context=None,
    )

    entry = make_entry(
        "राम",
        senses=(sense,),
    )

    builder = make_builder()

    builder.build(
        (
            make_lexicon(entry),
        ),
    )

    assert len(builder.context_index) == 0


# =========================================================
# Source Index
# =========================================================


def test_build_indexes_sense_source():
    source = make_source(
        "monier-williams",
    )

    sense = make_sense(
        source=source,
    )

    entry = make_entry(
        "राम",
        senses=(sense,),
    )

    builder = make_builder()

    builder.build(
        (
            make_lexicon(entry),
        ),
    )

    assert (
        sense
        in builder.source_index.lookup(
            "monier-williams",
        )
    )


def test_sense_without_source_is_not_added_to_source_index():
    sense = make_sense(
        source=None,
    )

    entry = make_entry(
        "राम",
        senses=(sense,),
    )

    builder = make_builder()

    builder.build(
        (
            make_lexicon(entry),
        ),
    )

    assert len(builder.source_index) == 0


# =========================================================
# Multiple Senses
# =========================================================


def test_multiple_senses_are_indexed():
    context = make_context(
        "context-1",
    )

    source = make_source(
        "source-1",
    )

    sense1 = make_sense(
        context=context,
        source=source,
        sense_id="sense-1",
    )

    sense2 = make_sense(
        context=context,
        source=source,
        sense_id="sense-2",
    )

    entry = make_entry(
        "राम",
        senses=(sense1, sense2),
    )

    builder = make_builder()

    builder.build(
        (
            make_lexicon(entry),
        ),
    )

    assert (
        builder.context_index.lookup(
            "context-1",
        )
        == (sense1, sense2)
    )

    assert (
        builder.source_index.lookup(
            "source-1",
        )
        == (sense1, sense2)
    )


# =========================================================
# Multiple Lexicons
# =========================================================


def test_build_processes_multiple_lexicons():
    first = make_lexicon(
        make_entry(
            "राम",
            lemma=make_lemma("राम"),
        )
    )

    second = CanonicalLexicon(
        identifier="test-lexicon-2",
        name="Second Test Lexicon",
        version="1.0",
    )

    second.add(
        make_entry(
            "हरि",
            lemma=make_lemma("हरि"),
        )
    )

    builder = make_builder()

    builder.build(
        (
            first,
            second,
        ),
    )

    assert builder.headword_index.lookup("राम")
    assert builder.headword_index.lookup("हरि")

    assert len(builder.lemma_index) == 2


# =========================================================
# Rebuild Semantics
# =========================================================


def test_build_replaces_previous_index_contents():
    first = make_lexicon(
        make_entry(
            "राम",
            lemma=make_lemma("राम"),
        )
    )

    second = CanonicalLexicon(
        identifier="test-lexicon-2",
        name="Second Test Lexicon",
        version="1.0",
    )

    second.add(
        make_entry(
            "हरि",
            lemma=make_lemma("हरि"),
        )
    )

    builder = make_builder()

    builder.build(
        (first,),
    )

    assert builder.headword_index.lookup("राम")

    builder.build(
        (second,),
    )

    assert (
        builder.headword_index.lookup("राम")
        is None
    )

    assert builder.headword_index.lookup("हरि")


def test_repeated_build_is_deterministic():
    lexicon = make_lexicon(
        make_entry(
            "राम",
            lemma=make_lemma("राम"),
        )
    )

    builder = make_builder()

    builder.build(
        (lexicon,),
    )

    first_summary = builder.summary()

    builder.build(
        (lexicon,),
    )

    second_summary = builder.summary()

    assert first_summary == second_summary


# =========================================================
# Clear
# =========================================================


def test_clear_removes_all_index_data():
    builder = make_builder()

    context = make_context()
    source = make_source()

    sense = make_sense(
        context=context,
        source=source,
    )

    entry = make_entry(
        "राम",
        lemma=make_lemma(),
        senses=(sense,),
    )

    builder.build(
        (
            make_lexicon(entry),
        ),
    )

    builder.clear()

    assert len(builder.headword_index) == 0
    assert len(builder.lemma_index) == 0
    assert len(builder.context_index) == 0
    assert len(builder.source_index) == 0


# =========================================================
# Diagnostics
# =========================================================


def test_summary_reports_all_indexes():
    builder = make_builder()

    context = make_context()
    source = make_source()

    sense = make_sense(
        context=context,
        source=source,
    )

    entry = make_entry(
        "राम",
        lemma=make_lemma(),
        senses=(sense,),
    )

    builder.build(
        (
            make_lexicon(entry),
        ),
    )

    assert builder.summary() == {
        "headwords": 1,
        "lemmas": 1,
        "contexts": 1,
        "sources": 1,
    }


def test_string_representation_contains_summary():
    builder = make_builder()

    text = str(builder)

    assert "CanonicalIndexBuilder" in text
    assert "headwords" in text
    assert "lemmas" in text
    assert "contexts" in text
    assert "sources" in text    
