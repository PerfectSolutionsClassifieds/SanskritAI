from SanskritAI.lexical.models.lexical_source import LexicalSource

def test_lexical_source_stores_identifier_and_name():
    source = LexicalSource(
        identifier="monier-williams",
        name="Monier-Williams Sanskrit-English Dictionary",
    )
    assert source.identifier == "monier-williams"
    assert source.name == "Monier-Williams Sanskrit-English Dictionary"

def test_lexical_source_default_optional_fields():
    source = LexicalSource(
        identifier="apte",
        name="Apte Sanskrit-English Dictionary",
    )
    assert source.version == ""
    assert source.description == ""
    assert source.publisher == ""
    assert source.editor == ""
    assert source.publication_year == ""
    assert source.website == ""

def test_lexical_source_preserves_full_source_information():
    source = LexicalSource(
        identifier="amara",
        name="Amarakośa",
        version="1.0",
        description="Classical Sanskrit thesaurus.",
        publisher="Test Publisher",
        editor="Test Editor",
        publication_year="2026",
        website="https://example.org/amara",
    )
    assert source.identifier == "amara"
    assert source.name == "Amarakośa"
    assert source.version == "1.0"
    assert source.description == "Classical Sanskrit thesaurus."
    assert source.publisher == "Test Publisher"
    assert source.editor == "Test Editor"
    assert source.publication_year == "2026"
    assert source.website == "https://example.org/amara"

def test_display_name_returns_name():
    source = LexicalSource(
        identifier="apte",
        name="Apte Sanskrit-English Dictionary",
    )
    assert source.display_name == "Apte Sanskrit-English Dictionary"

def test_display_text_without_version():
    source = LexicalSource(
        identifier="apte",
        name="Apte Sanskrit-English Dictionary",
    )
    assert source.display_text == "Apte Sanskrit-English Dictionary"

def test_display_text_with_version():
    source = LexicalSource(
        identifier="mw",
        name="Monier-Williams",
        version="1899",
    )
    assert source.display_text == "Monier-Williams (1899)"

def test_display_description_returns_description():
    source = LexicalSource(
        identifier="vacaspatyam",
        name="Vācaspatyam",
        description="Sanskrit lexicon.",
    )
    assert source.display_description == "Sanskrit lexicon."

def test_has_version():
    source_without = LexicalSource(
        identifier="apte",
        name="Apte",
    )
    source_with = LexicalSource(
        identifier="mw",
        name="Monier-Williams",
        version="1899",
    )
    assert source_without.has_version is False
    assert source_with.has_version is True

def test_has_publisher():
    source_without = LexicalSource(
        identifier="apte",
        name="Apte",
    )
    source_with = LexicalSource(
        identifier="apte",
        name="Apte",
        publisher="Publisher",
    )
    assert source_without.has_publisher is False
    assert source_with.has_publisher is True

def test_has_editor():
    source_without = LexicalSource(
        identifier="apte",
        name="Apte",
    )
    source_with = LexicalSource(
        identifier="apte",
        name="Apte",
        editor="Editor",
    )
    assert source_without.has_editor is False
    assert source_with.has_editor is True

def test_has_website():
    source_without = LexicalSource(
        identifier="apte",
        name="Apte",
    )
    source_with = LexicalSource(
        identifier="apte",
        name="Apte",
        website="https://example.org",
    )
    assert source_without.has_website is False
    assert source_with.has_website is True

def test_lexical_source_is_immutable():
    source = LexicalSource(
        identifier="amara",
        name="Amarakośa",
    )
    try:
        source.name = "Changed"
        assert False
    except AttributeError:
        assert True

def test_string_representation_without_version():
    source = LexicalSource(
        identifier="amara",
        name="Amarakośa",
    )
    assert str(source) == "Amarakośa"

def test_string_representation_with_version():
    source = LexicalSource(
        identifier="mw",
        name="Monier-Williams",
        version="1899",
    )
    assert str(source) == "Monier-Williams (1899)"
