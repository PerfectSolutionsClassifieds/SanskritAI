
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)


def test_context_creation():

    context = CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        section="Rudra Saṁhitā",
        chapter="12",
        chapter_title="A Chapter",
        verse="17",
        page_number=120,
        page_image="page_120.png",
    )

    assert context.corpus == "Purāṇa"
    assert context.work == "Śiva Purāṇa"
    assert context.section == "Rudra Saṁhitā"
    assert context.chapter == "12"
    assert context.chapter_title == "A Chapter"
    assert context.verse == "17"
    assert context.page_number == 120
    assert context.page_image == "page_120.png"


def test_context_identifier():

    context = CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        section="Rudra Saṁhitā",
        chapter="12",
        verse="17",
    )

    assert (
        context.identifier
        == "Purāṇa:Śiva Purāṇa:Rudra Saṁhitā:12:17"
    )


def test_context_identifier_omits_none_values():

    context = CanonicalContext(
        corpus="Veda",
        work="Ṛgveda",
        chapter="1",
    )

    assert context.identifier == "Veda:Ṛgveda:1"


def test_context_summary():

    context = CanonicalContext(
        corpus="Purāṇa",
        work="Bhāgavata Purāṇa",
        section="Skandha 10",
        chapter="29",
        verse="4",
    )

    assert context.summary() == {
        "corpus": "Purāṇa",
        "work": "Bhāgavata Purāṇa",
        "section": "Skandha 10",
        "chapter": "29",
        "verse": "4",
    }


def test_context_string():

    context = CanonicalContext(
        corpus="Purāṇa",
        work="Śiva Purāṇa",
        chapter="12",
        verse="17",
    )

    assert (
        str(context)
        == "CanonicalContext(Purāṇa:Śiva Purāṇa:12:17)"
    )


def test_context_is_immutable():

    context = CanonicalContext(
        corpus="Purāṇa",
    )

    with pytest.raises(Exception):
        context.corpus = "Veda"
