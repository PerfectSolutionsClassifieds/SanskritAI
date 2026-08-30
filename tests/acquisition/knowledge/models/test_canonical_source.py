
import pytest

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)


def test_source_creation():

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams Sanskrit-English Dictionary",
        short_name="MW",
        source_type="lexicon",
        author="Monier-Williams",
        publisher="Clarendon Press",
        edition="1st",
        publication_year=1899,
        version="1.0",
    )

    assert source.source_id == "mw"
    assert source.name == (
        "Monier-Williams Sanskrit-English Dictionary"
    )
    assert source.short_name == "MW"
    assert source.source_type == "lexicon"
    assert source.author == "Monier-Williams"


def test_display_name_prefers_short_name():

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams Sanskrit-English Dictionary",
        short_name="MW",
    )

    assert source.display_name == "MW"


def test_display_name_falls_back_to_name():

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams Sanskrit-English Dictionary",
    )

    assert (
        source.display_name
        == "Monier-Williams Sanskrit-English Dictionary"
    )


def test_is_online():

    source = CanonicalSource(
        source_id="mw",
        name="MW",
        website="https://example.org",
    )

    assert source.is_online is True


def test_is_online_false():

    source = CanonicalSource(
        source_id="mw",
        name="MW",
    )

    assert source.is_online is False


@pytest.mark.parametrize(
    "source_type, attribute",
    [
        ("lexicon", "is_lexicon"),
        ("primary_text", "is_primary_text"),
        ("grammar", "is_grammar"),
    ],
)
def test_source_type_classification(source_type, attribute):

    source = CanonicalSource(
        source_id="source",
        name="Source",
        source_type=source_type,
    )

    assert getattr(source, attribute) is True


def test_source_type_classification_is_case_insensitive():

    source = CanonicalSource(
        source_id="source",
        name="Source",
        source_type="LEXICON",
    )

    assert source.is_lexicon is True


def test_source_summary():

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams",
        source_type="lexicon",
        edition="1st",
        version="1.0",
        website="https://example.org",
    )

    assert source.summary() == {
        "source_id": "mw",
        "name": "Monier-Williams",
        "type": "lexicon",
        "edition": "1st",
        "version": "1.0",
        "online": True,
    }


def test_source_string():

    source = CanonicalSource(
        source_id="mw",
        name="Monier-Williams",
        short_name="MW",
    )

    assert str(source) == "CanonicalSource(MW)"


def test_source_immutability():

    source = CanonicalSource(
        source_id="mw",
        name="MW",
    )

    with pytest.raises(Exception):
        source.name = "Apte"
