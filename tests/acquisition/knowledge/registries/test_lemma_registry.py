
from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)

from SanskritAI.acquisition.knowledge.registries.lemma_registry import (
    LemmaRegistry,
)


# ============================================================
# Fixtures / Helpers
# ============================================================

def make_lemma(
    lemma: str,
    dhatu: str | None = None,
) -> CanonicalLemma:

    return CanonicalLemma(
        lemma=lemma,
        transliteration=None,
        language="sa",
        script="Devanagari",
        dhatu=dhatu,
    )


# ============================================================
# Initialization
# ============================================================

def test_registry_starts_empty():

    registry = LemmaRegistry()

    assert len(registry) == 0
    assert registry.all() == ()
    assert registry.lemma_ids == ()


# ============================================================
# Registration
# ============================================================

def test_register_lemma():

    registry = LemmaRegistry()

    lemma = make_lemma("गम्", "√गम्")

    registry.register(lemma)

    assert len(registry) == 1


def test_register_multiple_lemmas():

    registry = LemmaRegistry()

    lemma1 = make_lemma("गम्", "√गम्")
    lemma2 = make_lemma("भू", "√भू")

    registry.register(lemma1)
    registry.register(lemma2)

    assert len(registry) == 2


# ============================================================
# Lookup
# ============================================================

def test_lookup_registered_lemma():

    registry = LemmaRegistry()

    lemma = make_lemma("गम्", "√गम्")

    registry.register(lemma)

    result = registry.lookup("गम्")

    assert result is lemma


def test_lookup_missing_lemma_returns_none():

    registry = LemmaRegistry()

    assert registry.lookup("अज्ञात") is None


def test_lookup_by_text():

    registry = LemmaRegistry()

    lemma = make_lemma("गम्", "√गम्")

    registry.register(lemma)

    result = registry.lookup_by_text("गम्")

    assert result is lemma


def test_lookup_by_text_missing_returns_none():

    registry = LemmaRegistry()

    registry.register(
        make_lemma("गम्", "√गम्")
    )

    assert registry.lookup_by_text("भू") is None


# ============================================================
# Duplicate Registration
# ============================================================

def test_duplicate_registration_does_not_increase_count():

    registry = LemmaRegistry()

    lemma = make_lemma("गम्", "√गम्")

    registry.register(lemma)
    registry.register(lemma)

    assert len(registry) == 1


# ============================================================
# Enumeration
# ============================================================

def test_all_returns_tuple():

    registry = LemmaRegistry()

    registry.register(
        make_lemma("भू", "√भू")
    )

    registry.register(
        make_lemma("गम्", "√गम्")
    )

    result = registry.all()

    assert isinstance(result, tuple)


def test_all_is_sorted_by_lemma_text():

    registry = LemmaRegistry()

    lemma_bhu = make_lemma("भू", "√भू")
    lemma_gam = make_lemma("गम्", "√गम्")

    registry.register(lemma_bhu)
    registry.register(lemma_gam)

    result = registry.all()

    assert tuple(
        lemma.lemma
        for lemma in result
    ) == tuple(
        sorted(
            [lemma_bhu.lemma, lemma_gam.lemma]
        )
    )


def test_lemma_ids_are_sorted():

    registry = LemmaRegistry()

    registry.register(
        make_lemma("भू", "√भू")
    )

    registry.register(
        make_lemma("गम्", "√गम्")
    )

    assert registry.lemma_ids == tuple(
        sorted(registry.lemma_ids)
    )


# ============================================================
# Python Protocols
# ============================================================

def test_contains():

    registry = LemmaRegistry()

    lemma = make_lemma("गम्", "√गम्")

    registry.register(lemma)

    assert "गम्" in registry
    assert "अज्ञात" not in registry


def test_iteration():

    registry = LemmaRegistry()

    lemma1 = make_lemma("गम्", "√गम्")
    lemma2 = make_lemma("भू", "√भू")

    registry.register(lemma1)
    registry.register(lemma2)

    result = tuple(registry)

    assert len(result) == 2
    assert all(
        isinstance(item, CanonicalLemma)
        for item in result
    )


# ============================================================
# Diagnostics
# ============================================================

def test_summary():

    registry = LemmaRegistry()

    registry.register(
        make_lemma("गम्", "√गम्")
    )

    summary = registry.summary()

    assert summary["lemmas"] == 1
    assert "ids" in summary


# ============================================================
# String Representation
# ============================================================

def test_string_representation():

    registry = LemmaRegistry()

    registry.register(
        make_lemma("गम्", "√गम्")
    )

    assert str(registry) == "LemmaRegistry(1 lemmas)"
