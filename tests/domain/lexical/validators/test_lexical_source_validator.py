from __future__ import annotations

import pytest

from SanskritAI.domain.lexical.lexical_source import LexicalSource
from SanskritAI.domain.lexical.validators.lexical_source_validator import (
    LexicalSourceValidator,
)
from SanskritAI.models.enums.dictionary_source import DictionarySource


def make_source(
    *,
    source_id: str = "source-1",
    name: str = "Amarakosha",
    source_type: DictionarySource = DictionarySource.AMARAKOSHA,
    version: str = "",
    language: str = "sanskrit",
    script: str = "devanagari",
    description: str = "",
    url: str = "",
) -> LexicalSource:
    return LexicalSource(
        source_id=source_id,
        name=name,
        source_type=source_type,
        version=version,
        language=language,
        script=script,
        description=description,
        url=url,
    )


def issue_codes(result):
    return {issue.code for issue in result.issues}


def test_supports_lexical_source():
    source = make_source()

    assert LexicalSourceValidator.supports(source) is True


def test_does_not_support_unrelated_object():
    assert LexicalSourceValidator.supports(object()) is False


def test_valid_source_passes():
    result = LexicalSourceValidator().validate(
        make_source()
    )

    assert result.is_valid


def test_empty_source_id_is_invalid():
    result = LexicalSourceValidator().validate(
        make_source(source_id="")
    )

    assert not result.is_valid
    assert "LEXSRC001" in issue_codes(result)


def test_blank_source_id_is_invalid():
    result = LexicalSourceValidator().validate(
        make_source(source_id="   ")
    )

    assert not result.is_valid
    assert "LEXSRC001" in issue_codes(result)


def test_empty_name_is_invalid():
    result = LexicalSourceValidator().validate(
        make_source(name="")
    )

    assert not result.is_valid
    assert "LEXSRC002" in issue_codes(result)


def test_blank_name_is_invalid():
    result = LexicalSourceValidator().validate(
        make_source(name="   ")
    )

    assert not result.is_valid
    assert "LEXSRC002" in issue_codes(result)


def test_source_type_is_preserved():
    source = make_source(
        source_type=DictionarySource.MONIER_WILLIAMS
    )

    assert source.source_type is DictionarySource.MONIER_WILLIAMS


def test_language_is_required():
    result = LexicalSourceValidator().validate(
        make_source(language="")
    )

    assert not result.is_valid
    assert "LEXSRC004" in issue_codes(result)


def test_script_is_required():
    result = LexicalSourceValidator().validate(
        make_source(script="")
    )

    assert not result.is_valid
    assert "LEXSRC005" in issue_codes(result)


def test_version_is_optional():
    result = LexicalSourceValidator().validate(
        make_source(version="")
    )

    assert result.is_valid


def test_description_is_optional():
    result = LexicalSourceValidator().validate(
        make_source(description="")
    )

    assert result.is_valid


def test_https_url_is_valid():
    result = LexicalSourceValidator().validate(
        make_source(
            url="https://example.org/source"
        )
    )

    assert result.is_valid


def test_http_url_is_valid():
    result = LexicalSourceValidator().validate(
        make_source(
            url="http://example.org/source"
        )
    )

    assert result.is_valid


def test_non_http_url_produces_warning():
    result = LexicalSourceValidator().validate(
        make_source(
            url="example.org/source"
        )
    )

    assert result.is_valid
    assert "LEXSRC006" in issue_codes(result)


def test_display_name_uses_source_name():
    source = make_source(
        name="Monier-Williams"
    )

    assert source.display_name == "Monier-Williams"


def test_display_text_without_version():
    source = make_source(
        name="Amarakosha",
        version="",
    )

    assert source.display_text == "Amarakosha"


def test_display_text_with_version():
    source = make_source(
        name="Monier-Williams",
        version="1899",
    )

    assert source.display_text == "Monier-Williams (1899)"


def test_canonical_name_uses_dictionary_source():
    source = make_source(
        source_type=DictionarySource.VACHASPATYAM
    )

    assert source.canonical_name == "Vachaspatyam"


def test_to_dict_serializes_source():
    source = make_source(
        version="1.0",
        description="Lexical reference",
        url="https://example.org",
    )

    data = source.to_dict()

    assert data["source_id"] == "source-1"
    assert data["name"] == "Amarakosha"
    assert data["source_type"] == "Amarakosha"
    assert data["version"] == "1.0"
    assert data["language"] == "sanskrit"
    assert data["script"] == "devanagari"
    assert data["description"] == "Lexical reference"
    assert data["url"] == "https://example.org"


def test_source_is_immutable():
    source = make_source()

    with pytest.raises((AttributeError, TypeError)):
        source.name = "Changed"


def test_source_normalizes_text_fields():
    source = make_source(
        source_id="  source-1  ",
        name="  Amarakosha  ",
        version="  1.0  ",
        language="  sanskrit  ",
        script="  devanagari  ",
        description="  description  ",
        url="  https://example.org  ",
    )

    assert source.source_id == "source-1"
    assert source.name == "Amarakosha"
    assert source.version == "1.0"
    assert source.language == "sanskrit"
    assert source.script == "devanagari"
    assert source.description == "description"
    assert source.url == "https://example.org"


def test_has_version():
    assert make_source(version="1.0").has_version is True
    assert make_source(version="").has_version is False


def test_has_description():
    assert make_source(description="reference").has_description is True
    assert make_source(description="").has_description is False


def test_has_url():
    assert make_source(url="https://example.org").has_url is True
    assert make_source(url="").has_url is False


def test_string_representation_uses_display_text():
    source = make_source(
        name="Amarakosha",
        version="1.0",
    )

    assert str(source) == "Amarakosha (1.0)"
