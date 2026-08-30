
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_etymology import (
    CanonicalEtymology,
)

from SanskritAI.acquisition.knowledge.models.canonical_reference import (
    CanonicalReference,
)


def test_etymology_creation():

    reference = CanonicalReference(
        reference_id="ref-001",
        source_name="Aṣṭādhyāyī",
    )

    etymology = CanonicalEtymology(
        etymology_id="ety-001",
        entry_headword="गच्छति",
        dhatu="√गम्",
        pratyaya="तिप्",
        derivation="गम् + लट् + तिप्",
        explanation="Present tense derivation",
        source_tradition="Pāṇinian",
        references=(reference,),
    )

    assert etymology.etymology_id == "ety-001"
    assert etymology.entry_headword == "गच्छति"
    assert etymology.dhatu == "√गम्"
    assert etymology.pratyaya == "तिप्"
    assert etymology.reference_count == 1


def test_has_dhatu():

    etymology = CanonicalEtymology(
        etymology_id="e1",
        entry_headword="गच्छति",
        dhatu="√गम्",
    )

    assert etymology.has_dhatu is True


def test_has_dhatu_false():

    etymology = CanonicalEtymology(
        etymology_id="e1",
        entry_headword="राम",
    )

    assert etymology.has_dhatu is False


def test_has_pratyaya():

    etymology = CanonicalEtymology(
        etymology_id="e1",
        entry_headword="गच्छति",
        pratyaya="तिप्",
    )

    assert etymology.has_pratyaya is True


def test_reference_count():

    references = (
        CanonicalReference(
            reference_id="r1",
            source_name="Aṣṭādhyāyī",
        ),
        CanonicalReference(
            reference_id="r2",
            source_name="Dhātupāṭha",
        ),
    )

    etymology = CanonicalEtymology(
        etymology_id="e1",
        entry_headword="गच्छति",
        references=references,
    )

    assert etymology.reference_count == 2


def test_etymology_summary():

    etymology = CanonicalEtymology(
        etymology_id="e1",
        entry_headword="गच्छति",
        dhatu="√गम्",
        pratyaya="तिप्",
        source_tradition="Pāṇinian",
    )

    assert etymology.summary() == {
        "headword": "गच्छति",
        "dhatu": "√गम्",
        "pratyaya": "तिप्",
        "tradition": "Pāṇinian",
        "references": 0,
    }


def test_etymology_string():

    etymology = CanonicalEtymology(
        etymology_id="e1",
        entry_headword="गच्छति",
    )

    assert str(etymology) == "CanonicalEtymology(गच्छति)"


def test_etymology_immutability():

    etymology = CanonicalEtymology(
        etymology_id="e1",
        entry_headword="गच्छति",
    )

    with pytest.raises(Exception):
        etymology.entry_headword = "राम"
