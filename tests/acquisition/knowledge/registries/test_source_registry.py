
from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)

from SanskritAI.acquisition.knowledge.registries.source_registry import (
    SourceRegistry,
)


# ============================================================
# Fixtures / Helpers
# ============================================================

def make_source(
    source_id: str,
    name: str,
    short_name: str | None = None,
    source_type: str = "lexicon",
) -> CanonicalSource:

    return CanonicalSource(
        source_id=source_id,
        name=name,
        short_name=short_name,
        source_type=source_type,
        language="sa",
    )


# ============================================================
# Initialization
# ============================================================

def test_registry_starts_empty():

    registry = SourceRegistry()

    assert len(registry) == 0
    assert registry.all() == ()
    assert registry.source_ids == ()


# ============================================================
# Registration
# ============================================================

def test_register_source():

    registry = SourceRegistry()

    source = make_source(
        "mw",
        "Monier-Williams",
        "MW",
    )

    registry.register(source)

    assert len(registry) == 1


def test_register_multiple_sources():

    registry = SourceRegistry()

    source1 = make_source(
        "mw",
        "Monier-Williams",
        "MW",
    )

    source2 = make_source(
        "apte",
        "Apte",
        "Apte",
    )

    registry.register(source1)
    registry.register(source2)

    assert len(registry) == 2


# ============================================================
# Lookup
# ============================================================

def test_lookup_registered_source():

    registry = SourceRegistry()

    source = make_source(
        "mw",
        "Monier-Williams",
        "MW",
    )

    registry.register(source)

    result = registry.lookup("mw")

    assert result is source


def test_lookup_missing_source_returns_none():

    registry = SourceRegistry()

    assert registry.lookup("unknown") is None


def test_lookup_by_name():

    registry = SourceRegistry()

    source = make_source(
        "mw",
        "Monier-Williams",
        "MW",
    )

    registry.register(source)

    result = registry.lookup_by_name(
        "Monier-Williams"
    )

    assert result is source


def test_lookup_by_name_missing_returns_none():

    registry = SourceRegistry()

    registry.register(
        make_source(
            "mw",
            "Monier-Williams",
            "MW",
        )
    )

    assert registry.lookup_by_name(
        "Unknown"
    ) is None


def test_lookup_by_short_name():

    registry = SourceRegistry()

    source = make_source(
        "mw",
        "Monier-Williams",
        "MW",
    )

    registry.register(source)

    result = registry.lookup_by_short_name(
        "MW"
    )

    assert result is source


def test_lookup_by_short_name_missing_returns_none():

    registry = SourceRegistry()

    registry.register(
        make_source(
            "mw",
            "Monier-Williams",
            "MW",
        )
    )

    assert registry.lookup_by_short_name(
        "UNKNOWN"
    ) is None


# ============================================================
# Duplicate Registration
# ============================================================

def test_duplicate_registration_does_not_increase_count():

    registry = SourceRegistry()

    source = make_source(
        "mw",
        "Monier-Williams",
        "MW",
    )

    registry.register(source)
    registry.register(source)

    assert len(registry) == 1


# ============================================================
# Enumeration
# ============================================================

def test_all_returns_tuple():

    registry = SourceRegistry()

    registry.register(
        make_source(
            "mw",
            "Monier-Williams",
            "MW",
        )
    )

    result = registry.all()

    assert isinstance(result, tuple)


def test_all_is_sorted_by_display_name():

    registry = SourceRegistry()

    source1 = make_source(
        "z",
        "Zeta Source",
        "Z",
    )

    source2 = make_source(
        "a",
        "Alpha Source",
        "A",
    )

    registry.register(source1)
    registry.register(source2)

    result = registry.all()

    assert tuple(
        source.display_name
        for source in result
    ) == (
        "A",
        "Z",
    )


def test_source_ids_are_sorted():

    registry = SourceRegistry()

    registry.register(
        make_source(
            "z",
            "Zeta Source",
            "Z",
        )
    )

    registry.register(
        make_source(
            "a",
            "Alpha Source",
            "A",
        )
    )

    assert registry.source_ids == (
        "a",
        "z",
    )


# ============================================================
# Python Protocols
# ============================================================

def test_contains():

    registry = SourceRegistry()

    source = make_source(
        "mw",
        "Monier-Williams",
        "MW",
    )

    registry.register(source)

    assert "mw" in registry
    assert "unknown" not in registry


def test_iteration():

    registry = SourceRegistry()

    source1 = make_source(
        "mw",
        "Monier-Williams",
        "MW",
    )

    source2 = make_source(
        "apte",
        "Apte",
        "Apte",
    )

    registry.register(source1)
    registry.register(source2)

    result = tuple(registry)

    assert len(result) == 2

    assert all(
        isinstance(item, CanonicalSource)
        for item in result
    )


# ============================================================
# Diagnostics
# ============================================================

def test_summary():

    registry = SourceRegistry()

    registry.register(
        make_source(
            "mw",
            "Monier-Williams",
            "MW",
        )
    )

    summary = registry.summary()

    assert summary["sources"] == 1
    assert "ids" in summary


# ============================================================
# String Representation
# ============================================================

def test_string_representation():

    registry = SourceRegistry()

    registry.register(
        make_source(
            "mw",
            "Monier-Williams",
            "MW",
        )
    )

    assert str(registry) == (
        "SourceRegistry(1 sources)"
    )
