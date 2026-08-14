import pytest

from SanskritAI.lexical.models.lexical_source import LexicalSource
from SanskritAI.lexical.registries.lexical_source_catalog import (
    LexicalSourceCatalog,
)


def make_source(
    identifier="monier-williams",
    name="Monier-Williams Sanskrit-English Dictionary",
):
    return LexicalSource(
        identifier=identifier,
        name=name,
    )


def test_empty_catalog_has_no_sources():
    catalog = LexicalSourceCatalog()
    assert catalog.count == 0
    assert catalog.identifiers == ()
    assert catalog.sources == ()


def test_register_returns_source():
    catalog = LexicalSourceCatalog()
    source = make_source()
    assert catalog.register(source) is source


def test_register_stores_source_by_identifier():
    catalog = LexicalSourceCatalog()
    source = make_source()
    catalog.register(source)
    assert catalog.get("monier-williams") is source


def test_get_returns_none_for_unknown_source():
    catalog = LexicalSourceCatalog()
    assert catalog.get("unknown") is None


def test_require_returns_registered_source():
    catalog = LexicalSourceCatalog([make_source()])
    assert catalog.require("monier-williams").name == (
        "Monier-Williams Sanskrit-English Dictionary"
    )


def test_require_unknown_source_raises_key_error():
    catalog = LexicalSourceCatalog()
    with pytest.raises(KeyError, match="Unknown lexical source"):
        catalog.require("unknown")


def test_exists_reports_registered_source():
    catalog = LexicalSourceCatalog([make_source()])
    assert catalog.exists("monier-williams")
    assert not catalog.exists("unknown")


def test_contains_supports_identifier_membership():
    catalog = LexicalSourceCatalog([make_source()])
    assert "monier-williams" in catalog
    assert "unknown" not in catalog


def test_register_many_registers_all_sources():
    catalog = LexicalSourceCatalog()
    sources = [
        make_source("monier-williams", "Monier-Williams"),
        make_source("apte", "Apte"),
        make_source("amarakosha", "Amarakośa"),
    ]
    catalog.register_many(sources)
    assert catalog.count == 3
    assert catalog.identifiers == (
        "monier-williams",
        "apte",
        "amarakosha",
    )


def test_constructor_accepts_sources():
    sources = [
        make_source("apte", "Apte"),
        make_source("amarakosha", "Amarakośa"),
    ]
    catalog = LexicalSourceCatalog(sources)
    assert catalog.count == 2
    assert catalog.get("apte") is sources[0]
    assert catalog.get("amarakosha") is sources[1]


def test_duplicate_identifier_is_rejected():
    catalog = LexicalSourceCatalog([make_source()])
    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        catalog.register(make_source())


def test_empty_identifier_is_rejected():
    source = make_source(identifier="")
    catalog = LexicalSourceCatalog()
    with pytest.raises(
        ValueError,
        match="identifier",
    ):
        catalog.register(source)


def test_whitespace_identifier_is_rejected():
    source = make_source(identifier="   ")
    catalog = LexicalSourceCatalog()
    with pytest.raises(
        ValueError,
        match="identifier",
    ):
        catalog.register(source)


def test_identifier_lookup_is_trimmed():
    catalog = LexicalSourceCatalog([make_source()])
    assert catalog.get("  monier-williams  ") is not None
    assert catalog.require("  monier-williams  ").identifier == (
        "monier-williams"
    )


def test_non_string_identifier_is_rejected():
    catalog = LexicalSourceCatalog()
    with pytest.raises(TypeError, match="identifier"):
        catalog.get(123)


def test_non_lexical_source_is_rejected():
    catalog = LexicalSourceCatalog()
    with pytest.raises(
        TypeError,
        match="LexicalSource",
    ):
        catalog.register("monier-williams")


def test_identifiers_preserve_registration_order():
    catalog = LexicalSourceCatalog()
    catalog.register(make_source("apte", "Apte"))
    catalog.register(
        make_source(
            "monier-williams",
            "Monier-Williams",
        )
    )
    catalog.register(
        make_source(
            "amarakosha",
            "Amarakośa",
        )
    )
    assert catalog.identifiers == (
        "apte",
        "monier-williams",
        "amarakosha",
    )


def test_sources_preserve_registration_order():
    first = make_source("apte", "Apte")
    second = make_source(
        "monier-williams",
        "Monier-Williams",
    )
    catalog = LexicalSourceCatalog([first, second])
    assert catalog.sources == (first, second)


def test_iteration_returns_registered_sources():
    first = make_source("apte", "Apte")
    second = make_source(
        "amarakosha",
        "Amarakośa",
    )
    catalog = LexicalSourceCatalog([first, second])
    assert list(catalog) == [first, second]


def test_len_returns_source_count():
    catalog = LexicalSourceCatalog()
    assert len(catalog) == 0
    catalog.register(make_source())
    assert len(catalog) == 1


def test_remove_returns_removed_source():
    source = make_source()
    catalog = LexicalSourceCatalog([source])
    removed = catalog.remove("monier-williams")
    assert removed is source
    assert catalog.count == 0
    assert not catalog.exists("monier-williams")


def test_remove_unknown_source_raises_key_error():
    catalog = LexicalSourceCatalog()
    with pytest.raises(KeyError, match="Unknown lexical source"):
        catalog.remove("unknown")


def test_clear_removes_all_sources():
    catalog = LexicalSourceCatalog(
        [
            make_source("apte", "Apte"),
            make_source("amarakosha", "Amarakośa"),
        ]
    )
    catalog.clear()
    assert catalog.count == 0
    assert catalog.identifiers == ()
    assert catalog.sources == ()
