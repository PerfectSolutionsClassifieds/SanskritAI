from __future__ import annotations

from SanskritAI.domain.lexical.adapters import (
    MonierWilliamsRecord,
)
from SanskritAI.domain.lexical.adapters.monier_williams_mapper import (
    MonierWilliamsMapper,
)


def make_record() -> MonierWilliamsRecord:
    return MonierWilliamsRecord(
        headword="राम",
        transliteration="rāma",
        definition="pleasing, beautiful",
        grammatical_label="noun",
        source_id="mw:ram",
    )


def test_to_entry_preserves_source_information():
    entry = MonierWilliamsMapper.to_entry(
        make_record(),
    )

    assert entry.identifier == "mw:ram"
    assert entry.lemma == "राम"
    assert entry.language == "sa"
    assert entry.source == "monier-williams"
    assert entry.transliteration == "rāma"


def test_to_sense_preserves_definition():
    sense = MonierWilliamsMapper.to_sense(
        make_record(),
        entry_id="mw:ram",
    )

    assert sense.identifier == "mw:ram:1"
    assert sense.entry_id == "mw:ram"
    assert sense.meaning == "pleasing, beautiful"
    assert sense.language == "en"
    assert sense.source == "monier-williams"
    assert sense.grammatical_label == "noun"
