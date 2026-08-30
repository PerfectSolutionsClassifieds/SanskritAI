
from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)

from SanskritAI.acquisition.knowledge.registries.lexical_registry import (
    LexicalRegistry,
)


# ============================================================
# Fixtures / Helpers
# ============================================================

def make_lexicon(
    identifier: str,
    name: str,
    version: str = "1.0.0",
) -> CanonicalLexicon:

    return CanonicalLexicon(
        identifier=identifier,
        name=name,
        version=version,
        language="sa",
    )


# ============================================================
# Initialization
# ============================================================

def test_registry_starts_empty():

    registry = LexicalRegistry()

    assert len(registry) == 0
    assert registry.all() == ()
    assert registry.lexicon_ids == ()


# ============================================================
# Registration
# ============================================================

def test_register_lexicon():

    registry = LexicalRegistry()

    lexicon = make_lexicon(
        "mw",
        "Monier-Williams",
    )

    registry.register(lexicon)

    assert len(registry) == 1


def test_register_multiple_lexicons():

    registry = LexicalRegistry()

    lexicon1 = make_lexicon(
        "mw",
        "Monier-Williams",
    )

    lexicon2 = make_lexicon(
        "apte",
        "Apte",
    )

    registry.register(lexicon1)
    registry.register(lexicon2)

    assert len(registry) == 2


# ============================================================
# Lookup
# ============================================================

def test_lookup_registered_lexicon():

    registry = LexicalRegistry()

    lexicon = make_lexicon(
        "mw",
        "Monier-Williams",
    )

    registry.register(lexicon)

    result = registry.lookup("mw")

    assert result is lexicon


def test_lookup_missing_lexicon_returns_none():

    registry = LexicalRegistry()

    assert registry.lookup("unknown") is None


def test_lookup_by_name():

    registry = LexicalRegistry()

    lexicon = make_lexicon(
        "mw",
        "Monier-Williams",
    )

    registry.register(lexicon)

    result = registry.lookup_by_name(
        "Monier-Williams"
    )

    assert result is lexicon


def test_lookup_by_name_missing_returns_none():

    registry = LexicalRegistry()

    registry.register(
        make_lexicon(
            "mw",
            "Monier-Williams",
        )
    )

    assert registry.lookup_by_name(
        "Unknown"
    ) is None


# ============================================================
# Duplicate Registration
# ============================================================

def test_duplicate_registration_does_not_increase_count():

    registry = LexicalRegistry()

    lexicon = make_lexicon(
        "mw",
        "Monier-Williams",
    )

    registry.register(lexicon)
    registry.register(lexicon)

    assert len(registry) == 1


# ============================================================
# Enumeration
# ============================================================

def test_all_returns_tuple():

    registry = LexicalRegistry()

    registry.register(
        make_lexicon(
            "mw",
            "Monier-Williams",
        )
    )

    result = registry.all()

    assert isinstance(result, tuple)


def test_all_is_sorted_by_name():

    registry = LexicalRegistry()

    lexicon1 = make_lexicon(
        "z",
        "Z-Lexicon",
    )

    lexicon2 = make_lexicon(
        "a",
        "A-Lexicon",
    )

    registry.register(lexicon1)
    registry.register(lexicon2)

    result = registry.all()

    assert tuple(
        lexicon.name
        for lexicon in result
    ) == (
        "A-Lexicon",
        "Z-Lexicon",
    )


def test_lexicon_ids_are_sorted():

    registry = LexicalRegistry()

    registry.register(
        make_lexicon(
            "z",
            "Z-Lexicon",
        )
    )

    registry.register(
        make_lexicon(
            "a",
            "A-Lexicon",
        )
    )

    assert registry.lexicon_ids == (
        "a",
        "z",
    )


# ============================================================
# Python Protocols
# ============================================================

def test_contains():

    registry = LexicalRegistry()

    lexicon = make_lexicon(
        "mw",
        "Monier-Williams",
    )

    registry.register(lexicon)

    assert "mw" in registry
    assert "unknown" not in registry


def test_iteration():

    registry = LexicalRegistry()

    lexicon1 = make_lexicon(
        "mw",
        "Monier-Williams",
    )

    lexicon2 = make_lexicon(
        "apte",
        "Apte",
    )

    registry.register(lexicon1)
    registry.register(lexicon2)

    result = tuple(registry)

    assert len(result) == 2

    assert all(
        isinstance(item, CanonicalLexicon)
        for item in result
    )


# ============================================================
# Diagnostics
# ============================================================

def test_summary():

    registry = LexicalRegistry()

    registry.register(
        make_lexicon(
            "mw",
            "Monier-Williams",
        )
    )

    summary = registry.summary()

    assert summary["lexicons"] == 1
    assert "ids" in summary


# ============================================================
# String Representation
# ============================================================

def test_string_representation():

    registry = LexicalRegistry()

    registry.register(
        make_lexicon(
            "mw",
            "Monier-Williams",
        )
    )

    assert str(registry) == (
        "LexicalRegistry(1 lexicons)"
    )
