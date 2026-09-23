
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)


def test_lemma_creation():

    lemma = CanonicalLemma(
        lemma="गम्",
        transliteration="gam",
        dhatu="√गम्",
        part_of_speech="verb",
        lexical_category="verbal root",
    )

    assert lemma.lemma == "गम्"
    assert lemma.transliteration == "gam"
    assert lemma.dhatu == "√गम्"
    assert lemma.part_of_speech == "verb"
    assert lemma.lexical_category == "verbal root"


def test_lemma_defaults():

    lemma = CanonicalLemma(
        lemma="राम",
    )

    assert lemma.transliteration is None
    assert lemma.language == "sa"
    assert lemma.script == "Devanagari"
    assert lemma.dhatu is None
    assert lemma.part_of_speech is None
    assert lemma.lexical_category is None
    assert lemma.metadata == {}


def test_lemma_display_name():

    lemma = CanonicalLemma(
        lemma="गम्",
    )

    assert lemma.display_name == "गम्"


def test_lemma_summary():

    lemma = CanonicalLemma(
        lemma="गम्",
        dhatu="√गम्",
        part_of_speech="verb",
        lexical_category="verbal root",
    )

    assert lemma.summary() == {
        "lemma": "गम्",
        "dhatu": "√गम्",
        "part_of_speech": "verb",
        "category": "verbal root",
    }


def test_lemma_string():

    lemma = CanonicalLemma(
        lemma="गम्",
    )

    assert str(lemma) == "CanonicalLemma(गम्)"


def test_lemma_immutability():

    lemma = CanonicalLemma(
        lemma="गम्",
    )

    with pytest.raises(Exception):
        lemma.lemma = "भू"
