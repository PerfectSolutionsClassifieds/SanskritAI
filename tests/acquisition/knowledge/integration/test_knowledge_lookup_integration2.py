from __future__ import annotations

from SanskritAI.acquisition.knowledge.builders.canonical_index_builder import (
    CanonicalIndexBuilder,
)
from SanskritAI.acquisition.knowledge.indexes.context_index import (
    ContextIndex,
)
from SanskritAI.acquisition.knowledge.indexes.headword_index import (
    HeadwordIndex,
)
from SanskritAI.acquisition.knowledge.indexes.lemma_index import (
    LemmaIndex,
)
from SanskritAI.acquisition.knowledge.indexes.source_index import (
    SourceIndex,
)
from SanskritAI.acquisition.knowledge.lookup.lexical_lookup_engine import (
    LexicalLookupEngine,
)
from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)
from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)
from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)


def make_graph() -> tuple[
    CanonicalLexicon, CanonicalIndexBuilder, LexicalLookupEngine,
]:
    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams Sanskrit-English Dictionary",
        short_name="MW",
        source_type="lexicon",
        author="Monier-Williams",
        publication_year=1899,
        version="test-1.0",
    )

    rama_context = CanonicalContext(
        corpus="Purāṇa",
        work="Rāmāyaṇa",
        chapter="1",
        verse="1",
    )

    hari_context = CanonicalContext(
        corpus="Purāṇa",
        work="Bhāgavata Purāṇa",
        chapter="10",
        verse="14",
    )

    shiva_context = CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        chapter="12",
        verse="17",
    )

    rama_sense = CanonicalDictionarySense(
        sense_id="mw:MW-राम",
        entry_headword="राम",
        definition="Rama; a proper name",
        context=rama_context,
        source=source,
        part_of_speech="noun",
    )

    hari_sense = CanonicalDictionarySense(
        sense_id="mw:MW-हरि",
        entry_headword="हरि",
        definition="Hari; Vishnu",
        context=hari_context,
        source=source,
        part_of_speech="noun",
    )

    shiva_sense = CanonicalDictionarySense(
        sense_id="mw:MW-शिव",
        entry_headword="शिव",
        definition="auspicious; Shiva",
        context=shiva_context,
        source=source,
        part_of_speech="noun",
    )

    rama_entry = CanonicalDictionaryEntry(
        headword="राम",
        transliteration="rāma",
        lemma=CanonicalLemma(
            lemma="राम",
            transliteration="rāma",
            part_of_speech="noun",
        ),
        entry_type="noun",
        senses=(rama_sense,),
        source_name="Monier-Williams",
        source_version="test-1.0",
        source_record_id="MW-राम",
    )

    hari_entry = CanonicalDictionaryEntry(
        headword="हरि",
        transliteration="hari",
        lemma=CanonicalLemma(
            lemma="हरि",
            transliteration="hari",
            part_of_speech="noun",
        ),
        entry_type="noun",
        senses=(hari_sense,),
        source_name="Monier-Williams",
        source_version="test-1.0",
        source_record_id="MW-हरि",
    )

    shiva_entry = CanonicalDictionaryEntry(
        headword="शिव",
        transliteration="śiva",
        lemma=CanonicalLemma(
            lemma="शिव",
            transliteration="śiva",
            part_of_speech="noun",
        ),
        entry_type="noun",
        senses=(shiva_sense,),
        source_name="Monier-Williams",
        source_version="test-1.0",
        source_record_id="MW-शिव",
    )

    lexicon = CanonicalLexicon(
        identifier="mw.lookup.integration",
        name="Monier-Williams Lookup Integration",
        version="test-1.0",
        source="Monier-Williams",
        entries={
            "राम": rama_entry,
            "हरि": hari_entry,
            "शिव": shiva_entry,
        },
    )

    index_builder = CanonicalIndexBuilder(
        headword_index=HeadwordIndex(),
        lemma_index=LemmaIndex(),
        context_index=ContextIndex(),
        source_index=SourceIndex(),
    )

    index_builder.build((lexicon,))

    lookup = LexicalLookupEngine(
        headword_index=index_builder.headword_index,
        lemma_index=index_builder.lemma_index,
        context_index=index_builder.context_index,
        source_index=index_builder.source_index,
    )

    return lexicon, index_builder, lookup


def test_lookup_headword_returns_canonical_dictionary_entry():
    lexicon, _, lookup = make_graph()

    result = lookup.lookup_headword("राम")

    assert result is lexicon.get("राम")
    assert result.headword == "राम"
    assert result.lemma_text == "राम"


def test_lookup_lemma_returns_canonical_lemma():
    _, _, lookup = make_graph()

    result = lookup.lookup_lemma("राम")

    assert result is not None
    assert isinstance(result, CanonicalLemma)
    assert result.lemma == "राम"


def test_lookup_lemma_text_returns_canonical_lemma():
    _, _, lookup = make_graph()

    result = lookup.lookup_lemma_text("हरि")

    assert result is not None
    assert result.lemma == "हरि"


def test_lookup_context_returns_senses():
    _, _, lookup = make_graph()

    context_id = "Purāṇa:Rāmāyaṇa:1:1"

    result = lookup.lookup_context(context_id)

    assert isinstance(result, tuple)
    assert len(result) == 1

    sense = result[0]

    assert isinstance(sense, CanonicalDictionarySense)
    assert sense.entry_headword == "राम"


def test_lookup_context_for_purana():
    _, _, lookup = make_graph()

    result = lookup.contexts_for_purana("Purāṇa")

    assert isinstance(result, tuple)

    # The context index is built from the three canonical contexts.
    assert len(result) == 3


def test_lookup_context_for_chapter():
    _, _, lookup = make_graph()

    result = lookup.contexts_for_chapter(
        "Purāṇa:Rāmāyaṇa:1"
    )

    assert isinstance(result, tuple)
    assert len(result) == 1
    assert result[0].verse == "1"


def test_lookup_context_for_sloka():
    _, _, lookup = make_graph()

    result = lookup.contexts_for_sloka(
        "Purāṇa:Rāmāyaṇa:1:1"
    )

    assert isinstance(result, tuple)
    assert len(result) == 1
    assert result[0].verse == "1"


def test_lookup_source():
    _, _, lookup = make_graph()

    result = lookup.lookup_source("mw")

    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 1

    assert result[0].entry_headword == "राम"


def test_lookup_source_name():
    _, _, lookup = make_graph()

    result = lookup.lookup_source_name(
        "Monier-Williams Sanskrit-English Dictionary"
    )

    assert isinstance(result, tuple)
    assert len(result) == 3


def test_lookup_source_short_name():
    _, _, lookup = make_graph()

    result = lookup.lookup_source_short_name("MW")

    assert isinstance(result, tuple)
    assert len(result) == 3


def test_prefix_search():
    _, _, lookup = make_graph()

    result = lookup.prefix_search("रा")

    assert isinstance(result, tuple)
    assert len(result) >= 1

    assert any(
        entry.headword == "राम" for entry in result
    )


def test_unified_search():
    _, _, lookup = make_graph()

    result = lookup.search("राम")

    assert set(result.keys()) == {
        "headword",
        "lemma",
        "prefix_matches",
    }

    assert result["headword"] is not None
    assert result["lemma"] is not None
    assert result["lemma"].lemma == "राम"

    assert isinstance(
        result["prefix_matches"],
        tuple,
    )


def test_missing_lookup_returns_empty_or_none_without_error():
    _, _, lookup = make_graph()

    assert lookup.lookup_headword("अज्ञात") is None
    assert lookup.lookup_lemma("अज्ञात") is None
    assert lookup.lookup_lemma_text("अज्ञात") is None

    assert lookup.lookup_context("missing-context") == ()
    assert lookup.lookup_source("missing-source") == ()
