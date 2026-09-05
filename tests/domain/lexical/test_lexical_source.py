
from SanskritAI.domain.lexical.lexical_source import LexicalSource
from SanskritAI.models.enums.dictionary_source import DictionarySource


def test_lexical_source_can_be_created():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    assert source.source_id == "mw"
    assert source.name == "Monier-Williams"


def test_lexical_source_defaults():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    assert source.source_type == DictionarySource.UNKNOWN
    assert source.version == ""
    assert source.language == "sanskrit"
    assert source.script == "devanagari"
    assert source.description == ""
    assert source.url == ""


def test_lexical_source_strips_string_fields():
    source = LexicalSource(
        source_id="  mw  ",
        name="  Monier-Williams  ",
        version="  1899  ",
        language="  sanskrit  ",
        script="  devanagari  ",
        description="  Sanskrit-English dictionary  ",
        url="  https://example.org/mw  ",
    )

    assert source.source_id == "mw"
    assert source.name == "Monier-Williams"
    assert source.version == "1899"
    assert source.language == "sanskrit"
    assert source.script == "devanagari"
    assert source.description == "Sanskrit-English dictionary"
    assert source.url == "https://example.org/mw"


def test_display_name():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    assert source.display_name == "Monier-Williams"


def test_display_text_without_version():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    assert source.display_text == "Monier-Williams"


def test_display_text_with_version():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
        version="1899",
    )

    assert source.display_text == "Monier-Williams (1899)"


def test_display_description():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
        description="Sanskrit-English dictionary",
    )

    assert source.display_description == "Sanskrit-English dictionary"


def test_has_version():
    without_version = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    with_version = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
        version="1899",
    )

    assert without_version.has_version is False
    assert with_version.has_version is True


def test_has_description():
    without_description = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    with_description = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
        description="Sanskrit-English dictionary",
    )

    assert without_description.has_description is False
    assert with_description.has_description is True


def test_has_url():
    without_url = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    with_url = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
        url="https://example.org/mw",
    )

    assert without_url.has_url is False
    assert with_url.has_url is True


def test_canonical_name_uses_dictionary_source():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
        source_type=DictionarySource.MONIER_WILLIAMS,
    )

    assert source.canonical_name == DictionarySource.MONIER_WILLIAMS.value


def test_to_dict():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
        source_type=DictionarySource.MONIER_WILLIAMS,
        version="1899",
        language="sanskrit",
        script="devanagari",
        description="Sanskrit-English dictionary",
        url="https://example.org/mw",
    )

    assert source.to_dict() == {
        "source_id": "mw",
        "name": "Monier-Williams",
        "source_type": DictionarySource.MONIER_WILLIAMS.value,
        "version": "1899",
        "language": "sanskrit",
        "script": "devanagari",
        "description": "Sanskrit-English dictionary",
        "url": "https://example.org/mw",
    }


def test_string_representation_without_version():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    assert str(source) == "Monier-Williams"


def test_string_representation_with_version():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
        version="1899",
    )

    assert str(source) == "Monier-Williams (1899)"


def test_lexical_source_is_immutable():
    source = LexicalSource(
        source_id="mw",
        name="Monier-Williams",
    )

    try:
        source.name = "Changed"
        assert False, "LexicalSource should be immutable"
    except AttributeError:
        pass
