
from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)


# =========================================================
# Construction
# =========================================================

def test_canonical_lemma_minimal_construction():
    lemma = CanonicalLemma(
        lemma="गम्",
    )

    assert lemma.lemma == "गम्"
    assert lemma.transliteration is None
    assert lemma.language == "sa"
    assert lemma.script == "Devanagari"
    assert lemma.dhatu is None
    assert lemma.part_of_speech is None
    assert lemma.lexical_category is None
    assert lemma.metadata == {}


def test_canonical_lemma_full_construction():
    lemma = CanonicalLemma(
        lemma="गम्",
        transliteration="gam",
        language="sa",
        script="Devanagari",
        dhatu="√गम्",
        part_of_speech="verb",
        lexical_category="verbal root",
        metadata={
            "source": "Dhātupāṭha",
            "gana": "1",
        },
    )

    assert lemma.lemma == "गम्"
    assert lemma.transliteration == "gam"
    assert lemma.language == "sa"
    assert lemma.script == "Devanagari"
    assert lemma.dhatu == "√गम्"
    assert lemma.part_of_speech == "verb"
    assert lemma.lexical_category == "verbal root"
    assert lemma.metadata["source"] == "Dhātupāṭha"
    assert lemma.metadata["gana"] == "1"


# =========================================================
# Defaults
# =========================================================

def test_canonical_lemma_default_language():
    lemma = CanonicalLemma("गम्")

    assert lemma.language == "sa"


def test_canonical_lemma_default_script():
    lemma = CanonicalLemma("गम्")

    assert lemma.script == "Devanagari"


def test_canonical_lemma_default_metadata_is_independent():
    lemma1 = CanonicalLemma("गम्")
    lemma2 = CanonicalLemma("भू")

    assert lemma1.metadata == {}
    assert lemma2.metadata == {}
    assert lemma1.metadata is not lemma2.metadata


# =========================================================
# Summary
# =========================================================

def test_canonical_lemma_summary():
    lemma = CanonicalLemma(
        lemma="गम्",
        dhatu="√गम्",
        part_of_speech="verb",
        lexical_category="verbal root",
    )

    result = lemma.summary()

    assert result == {
        "lemma": "गम्",
        "dhatu": "√गम्",
        "part_of_speech": "verb",
        "category": "verbal root",
    }


def test_canonical_lemma_summary_with_defaults():
    lemma = CanonicalLemma(
        lemma="राम",
    )

    result = lemma.summary()

    assert result == {
        "lemma": "राम",
        "dhatu": None,
        "part_of_speech": None,
        "category": None,
    }


# =========================================================
# Convenience
# =========================================================

def test_canonical_lemma_display_name():
    lemma = CanonicalLemma(
        lemma="गम्",
    )

    assert lemma.display_name == "गम्"


def test_canonical_lemma_string_representation():
    lemma = CanonicalLemma(
        lemma="गम्",
    )

    assert str(lemma) == "CanonicalLemma(गम्)"


# =========================================================
# Immutability
# =========================================================

def test_canonical_lemma_is_frozen():
    lemma = CanonicalLemma(
        lemma="गम्",
    )

    try:
        lemma.lemma = "भू"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "CanonicalLemma should be immutable"
        )


# =========================================================
# Equality
# =========================================================

def test_canonical_lemma_equality():
    lemma1 = CanonicalLemma(
        lemma="गम्",
        transliteration="gam",
        dhatu="√गम्",
    )

    lemma2 = CanonicalLemma(
        lemma="गम्",
        transliteration="gam",
        dhatu="√गम्",
    )

    assert lemma1 == lemma2


def test_canonical_lemma_inequality():
    lemma1 = CanonicalLemma(
        lemma="गम्",
    )

    lemma2 = CanonicalLemma(
        lemma="भू",
    )

    assert lemma1 != lemma2
