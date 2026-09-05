
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


def test_full_monier_williams_to_default_lexical_repository():
    record = MonierWilliamsRecord(
        headword="राम",
        transliteration="rāma",
        definition="Rama",
        grammatical_label="m.",
        grammatical_category="noun",
        source="Monier-Williams",
        source_id="MW-001",
        source_reference="MW:001",
        raw_text="राम — Rama",
        homonym="1",
    )

    entry = MonierWilliamsMapper.to_entry(record)

    lexicon = CanonicalLexicon(
        identifier="mw.test",
        name="Monier-Williams Test",
        version="1.0.0",
        language="sa",
        source="Monier-Williams",
        entries={
            entry.headword: entry,
        },
    )

    knowledge = CanonicalKnowledgeRepository()

    knowledge.add_lexicon(lexicon)

    lexical_repository = knowledge.lexical_repository

    # --------------------------------------------------------
    # Repository identity
    # --------------------------------------------------------

    assert lexical_repository.repository is knowledge

    # --------------------------------------------------------
    # Entry lookup
    # --------------------------------------------------------

    result = lexical_repository.get_entry("राम")

    assert result is entry

    # --------------------------------------------------------
    # Lemma lookup
    # --------------------------------------------------------

    results = lexical_repository.find_entries_by_lemma("राम")

    assert results == (entry,)

    # --------------------------------------------------------
    # Word-form lookup
    # --------------------------------------------------------

    results = lexical_repository.find_entries_by_word_form("राम")

    assert results == (entry,)

    # --------------------------------------------------------
    # Sense lookup
    # --------------------------------------------------------

    senses = lexical_repository.find_senses("राम")

    assert len(senses) == 1
    assert senses[0].definition == "Rama"

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    results = lexical_repository.search("rāma")

    assert results == (entry,)

    # --------------------------------------------------------
    # Enumeration
    # --------------------------------------------------------

    assert lexical_repository.all_entries() == (entry,)

    # --------------------------------------------------------
    # Cardinality
    # --------------------------------------------------------

    assert lexical_repository.count == 1
