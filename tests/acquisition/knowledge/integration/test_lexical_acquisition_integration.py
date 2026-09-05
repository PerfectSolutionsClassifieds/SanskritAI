
from __future__ import annotations

from pathlib import Path

from SanskritAI.acquisition.knowledge.connectors.monier_williams_connector import (
    MonierWilliamsConnector,
)
from SanskritAI.acquisition.knowledge.models.canonical_lexical_record import (
    CanonicalLexicalRecord,
)
from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)


def make_source(tmp_path: Path) -> Path:
    """
    Create a deterministic miniature lexical source.

    The current Monier-Williams parser contract is intentionally
    structural: one non-empty line is one record and the first
    whitespace-separated token becomes the headword.
    """
    source = tmp_path / "mw_test.txt"

    source.write_text(
        "राम proper name Rama\n"
        "हरि Vishnu Hari\n"
        "शिव auspicious Shiva\n",
        encoding="utf-8",
    )

    return source


def test_connector_to_raw_entries_to_canonical_records(tmp_path: Path):
    """
    Integration path:

        Raw source
            ↓
        Connector
            ↓
        Parser
            ↓
        RawLexicalEntry
            ↓
        Transformer
            ↓
        CanonicalLexicalRecord
    """
    source = make_source(tmp_path)

    connector = MonierWilliamsConnector(
        source_name="Monier-Williams",
        source_version="test-1.0",
        resource=source,
    )

    # ---------------------------------------------------------
    # Connector
    # ---------------------------------------------------------
    connector.connect()

    fetched = connector.fetch()

    assert fetched == source
    assert fetched.exists()

    # ---------------------------------------------------------
    # Parser
    # ---------------------------------------------------------
    raw_entries = connector.parse(fetched)

    assert isinstance(raw_entries, tuple)
    assert len(raw_entries) == 3
    assert all(isinstance(entry, RawLexicalEntry) for entry in raw_entries)

    assert [entry.headword for entry in raw_entries] == [
        "राम",
        "हरि",
        "शिव",
    ]

    assert raw_entries[0].source_name == "Monier-Williams"
    assert raw_entries[0].source_version == "test-1.0"
    assert raw_entries[0].raw_text == "राम proper name Rama"

    # ---------------------------------------------------------
    # Transformer
    # ---------------------------------------------------------
    canonical_records = connector.transform(raw_entries)

    assert isinstance(canonical_records, tuple)
    assert len(canonical_records) == 3
    assert all(
        isinstance(record, CanonicalLexicalRecord)
        for record in canonical_records
    )

    assert [record.headword for record in canonical_records] == [
        "राम",
        "हरि",
        "शिव",
    ]

    assert canonical_records[0].definition == "राम proper name Rama"
    assert canonical_records[0].source_name == "Monier-Williams"
    assert canonical_records[0].source_version == "test-1.0"

    # ---------------------------------------------------------
    # Validation / publication
    # ---------------------------------------------------------
    validated = connector.validate(canonical_records)
    published = connector.publish(validated)

    assert validated == canonical_records
    assert published == canonical_records


def test_connector_discovery_reports_local_resource(tmp_path: Path):
    source = make_source(tmp_path)

    connector = MonierWilliamsConnector(
        source_name="Monier-Williams",
        source_version="test-1.0",
        resource=source,
    )

    result = connector.discover()

    assert result["source_name"] == "Monier-Williams"
    assert result["source_version"] == "test-1.0"
    assert result["resource"] == str(source)
    assert result["available"] is True


def test_acquisition_preserves_source_provenance(tmp_path: Path):
    source = make_source(tmp_path)

    connector = MonierWilliamsConnector(
        source_name="Monier-Williams",
        source_version="test-1.0",
        resource=source,
    )

    raw_entries = connector.parse(connector.acquire(tmp_path))
    canonical_records = connector.transform(raw_entries)

    for raw, canonical in zip(raw_entries, canonical_records):
        assert canonical.source_name == raw.source_name
        assert canonical.source_version == raw.source_version
        assert canonical.source_record_id == raw.source_record_id
        assert canonical.headword == raw.headword
        
