
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_reference import (
    CanonicalReference,
)


def test_reference_creation():

    reference = CanonicalReference(
        reference_id="ref-001",
        source_name="Śiva Purāṇa",
        work="Rudra Saṁhitā",
        section="Section 1",
        chapter="12",
        verse="17",
        page="120",
        line="5",
        edition="Critical Edition",
        publication_year=2020,
    )

    assert reference.reference_id == "ref-001"
    assert reference.source_name == "Śiva Purāṇa"
    assert reference.work == "Rudra Saṁhitā"
    assert reference.chapter == "12"
    assert reference.verse == "17"


def test_reference_location():

    reference = CanonicalReference(
        reference_id="ref-001",
        source_name="Śiva Purāṇa",
        work="Rudra Saṁhitā",
        section="Section 1",
        chapter="12",
        verse="17",
        page="120",
    )

    assert (
        reference.location
        == "Rudra Saṁhitā : Section 1 : 12 : 17 : 120"
    )


def test_reference_location_with_missing_fields():

    reference = CanonicalReference(
        reference_id="ref-001",
        source_name="MW",
        work="Dictionary",
        page="100",
    )

    assert reference.location == "Dictionary : 100"


def test_reference_summary():

    reference = CanonicalReference(
        reference_id="ref-001",
        source_name="MW",
        work="Dictionary",
        chapter="1",
        verse="2",
        page="100",
    )

    assert reference.summary() == {
        "source": "MW",
        "work": "Dictionary",
        "chapter": "1",
        "verse": "2",
        "page": "100",
    }


def test_reference_string_with_location():

    reference = CanonicalReference(
        reference_id="ref-001",
        source_name="MW",
        work="Dictionary",
        page="100",
    )

    assert str(reference) == "MW (Dictionary : 100)"


def test_reference_string_without_location():

    reference = CanonicalReference(
        reference_id="ref-001",
        source_name="MW",
    )

    assert str(reference) == "MW"


def test_reference_immutability():

    reference = CanonicalReference(
        reference_id="ref-001",
        source_name="MW",
    )

    with pytest.raises(Exception):
        reference.source_name = "Apte"
