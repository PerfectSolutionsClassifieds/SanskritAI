
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_example import (
    CanonicalExample,
)

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)

from SanskritAI.acquisition.knowledge.models.canonical_reference import (
    CanonicalReference,
)


def test_example_creation():

    context = CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        chapter="12",
        verse="17",
    )

    reference = CanonicalReference(
        reference_id="ref-001",
        source_name="Śiva Purāṇa",
        work="Rudra Saṁhitā",
        chapter="12",
        verse="17",
    )

    example = CanonicalExample(
        example_id="ex-001",
        entry_headword="राम",
        sense_id="sense-001",
        sanskrit_text="रामः वनं गच्छति।",
        transliteration="rāmaḥ vanaṃ gacchati.",
        translation="Rama goes to the forest.",
        explanation="Example usage.",
        context=context,
        references=(reference,),
    )

    assert example.example_id == "ex-001"
    assert example.entry_headword == "राम"
    assert example.sense_id == "sense-001"
    assert example.sanskrit_text == "रामः वनं गच्छति।"
    assert example.transliteration == "rāmaḥ vanaṃ gacchati."
    assert example.translation == "Rama goes to the forest."


def test_has_translation():

    example = CanonicalExample(
        example_id="e1",
        entry_headword="राम",
        sense_id="s1",
        sanskrit_text="रामः।",
        translation="Rama.",
    )

    assert example.has_translation is True


def test_has_translation_false():

    example = CanonicalExample(
        example_id="e1",
        entry_headword="राम",
        sense_id="s1",
        sanskrit_text="रामः।",
    )

    assert example.has_translation is False


def test_has_context():

    context = CanonicalContext(
        corpus="Purāṇa",
    )

    example = CanonicalExample(
        example_id="e1",
        entry_headword="राम",
        sense_id="s1",
        sanskrit_text="रामः।",
        context=context,
    )

    assert example.has_context is True


def test_reference_count():

    references = (
        CanonicalReference(
            reference_id="r1",
            source_name="Source 1",
        ),
        CanonicalReference(
            reference_id="r2",
            source_name="Source 2",
        ),
    )

    example = CanonicalExample(
        example_id="e1",
        entry_headword="राम",
        sense_id="s1",
        sanskrit_text="रामः।",
        references=references,
    )

    assert example.reference_count == 2


def test_example_summary():

    example = CanonicalExample(
        example_id="e1",
        entry_headword="राम",
        sense_id="s1",
        sanskrit_text="रामः।",
    )

    assert example.summary() == {
        "example_id": "e1",
        "headword": "राम",
        "sense_id": "s1",
        "references": 0,
        "has_context": False,
    }


def test_example_string():

    example = CanonicalExample(
        example_id="e1",
        entry_headword="राम",
        sense_id="s1",
        sanskrit_text="रामः।",
    )

    assert str(example) == "CanonicalExample(राम)"


def test_example_immutability():

    example = CanonicalExample(
        example_id="e1",
        entry_headword="राम",
        sense_id="s1",
        sanskrit_text="रामः।",
    )

    with pytest.raises(Exception):
        example.entry_headword = "हरि"
