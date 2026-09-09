
from SanskritAI.acquisition.knowledge.canonical_knowledge_repository import (
    CanonicalKnowledgeRepository,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)

from SanskritAI.domain.lexical.adapters.monier_williams_mapper import (
    MonierWilliamsMapper,
)
from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)


def make_record(
    headword: str,
    transliteration: str,
    definition: str,
    source_id: str,
):
    return MonierWilliamsRecord(
        headword=headword,
        transliteration=transliteration,
        definition=definition,
        grammatical_label="m.",
        grammatical_category="noun",
        source="Monier-Williams",
        source_id=source_id,
        source_reference=f"MW:{source_id}",
        raw_text=definition,
        homonym="1",
    )


def test_monier_williams_to_canonical_repository():
    records = (
        make_record(
            "राम",
            "rāma",
            "Rama",
            "MW-001",
        ),
        make_record(
            "हरि",
            "hari",
            "Hari",
            "MW-002",
        ),
    )

    entries = MonierWilliamsMapper.to_entries(records)

    lexicon = CanonicalLexicon(
        identifier="mw.test",
        name="Monier-Williams Test",
        version="1.0.0",
        language="sa",
        source="Monier-Williams",
        entries={
            entry.headword: entry
            for entry in entries
        },
    )

    repository = CanonicalKnowledgeRepository()

    repository.add_lexicon(lexicon)

    assert len(repository.all_lexicons()) == 1
    assert repository.lexical_entry_count == 2

    rama = repository.get_entry("राम")

    assert rama is not None
    assert rama.headword == "राम"
    assert rama.lemma == "राम"

    senses = repository.find_senses("राम")

    assert len(senses) == 1
    assert senses[0].definition == "Rama"


def test_monier_williams_entries_are_searchable_through_repository():
    record = make_record(
        "राम",
        "rāma",
        "Rama",
        "MW-001",
    )

    entry = MonierWilliamsMapper.to_entry(record)

    lexicon = CanonicalLexicon(
        identifier="mw.test",
        name="Monier-Williams Test",
        version="1.0.0",
        entries={
            entry.headword: entry,
        },
    )

    repository = CanonicalKnowledgeRepository()
    repository.add_lexicon(lexicon)

    assert repository.find_entries_by_lemma("राम") == (
        entry,
    )

    assert repository.find_entries_by_word_form("राम") == (
        entry,
    )

    assert repository.search("rāma") == (
        entry,
    )
