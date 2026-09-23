
from __future__ import annotations

import pytest

from SanskritAI.common.identifiers.document_id import DocumentId
from SanskritAI.corpus.builders.document_builder import (
    DocumentBuilder,
)
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.document_metadata import (
    DocumentMetadata,
)
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import (
    SectionMetadata,
)


# ============================================================
# Construction / Factory
# ============================================================


def test_create_instance_returns_document():
    builder = DocumentBuilder()

    assert isinstance(builder.instance(), Document)


def test_create_instance_generates_document_id():
    builder = DocumentBuilder()

    assert isinstance(
        builder.instance().id,
        DocumentId,
    )


def test_create_instance_initializes_document_metadata():
    builder = DocumentBuilder()

    assert isinstance(
        builder.instance().metadata,
        DocumentMetadata,
    )


# ============================================================
# Inherited Fluent Metadata API
# ============================================================


def test_with_title_is_fluent():
    builder = DocumentBuilder()

    result = builder.with_title("Adi Parva")

    assert result is builder


def test_with_description_is_fluent():
    builder = DocumentBuilder()

    result = builder.with_description(
        "First major section"
    )

    assert result is builder


def test_with_identifier_is_fluent():
    builder = DocumentBuilder()

    result = builder.with_identifier(
        "mahabharata-adi-parva"
    )

    assert result is builder


def test_with_sequence_number_is_fluent():
    builder = DocumentBuilder()

    result = builder.with_sequence_number(1)

    assert result is builder


def test_with_parent_identifier_is_fluent():
    builder = DocumentBuilder()

    result = builder.with_parent_identifier(
        "mahabharata"
    )

    assert result is builder


# ============================================================
# Document Metadata
# ============================================================


def test_with_title_sets_title():
    builder = DocumentBuilder().with_title(
        "Adi Parva"
    )

    assert builder.instance().metadata.title == "Adi Parva"


def test_with_document_type_sets_document_type():
    builder = DocumentBuilder().with_document_type(
        "Purana"
    )

    assert (
        builder.instance().metadata.document_type
        == "Purana"
    )


def test_with_page_range_sets_page_range():
    builder = DocumentBuilder().with_page_range(
        10,
        50,
    )

    metadata = builder.instance().metadata

    assert metadata.start_page == 10
    assert metadata.end_page == 50


def test_with_page_range_accepts_none():
    builder = DocumentBuilder().with_page_range(
        None,
        None,
    )

    metadata = builder.instance().metadata

    assert metadata.start_page is None
    assert metadata.end_page is None


def test_with_publisher_sets_publisher():
    builder = DocumentBuilder().with_publisher(
        "Sanskrit Research Institute"
    )

    assert (
        builder.instance().metadata.publisher
        == "Sanskrit Research Institute"
    )


def test_with_edition_sets_edition():
    builder = DocumentBuilder().with_edition(
        "Critical Edition"
    )

    assert (
        builder.instance().metadata.edition
        == "Critical Edition"
    )


def test_with_publication_year_sets_year():
    builder = DocumentBuilder().with_publication_year(
        "2026"
    )

    assert (
        builder.instance().metadata.publication_year
        == "2026"
    )


# ============================================================
# Contributors
# ============================================================


def test_add_author_is_fluent():
    builder = DocumentBuilder()

    result = builder.add_author("Author One")

    assert result is builder


def test_add_author_appends_author():
    builder = DocumentBuilder()

    builder.add_author("Author One")
    builder.add_author("Author Two")

    assert builder.instance().metadata.authors == [
        "Author One",
        "Author Two",
    ]


def test_add_editor_appends_editor():
    builder = DocumentBuilder()

    builder.add_editor("Editor One")
    builder.add_editor("Editor Two")

    assert builder.instance().metadata.editors == [
        "Editor One",
        "Editor Two",
    ]


def test_add_translator_appends_translator():
    builder = DocumentBuilder()

    builder.add_translator("Translator One")
    builder.add_translator("Translator Two")

    assert builder.instance().metadata.translators == [
        "Translator One",
        "Translator Two",
    ]


# ============================================================
# Sections
# ============================================================


def make_section(identifier: str) -> Section:
    return Section(
        identifier=identifier,
        metadata=SectionMetadata(),
    )


def test_add_section_is_fluent():
    builder = DocumentBuilder()
    section = make_section("section-1")

    result = builder.add_section(section)

    assert result is builder


def test_add_section_adds_section():
    builder = DocumentBuilder()
    section = make_section("section-1")

    builder.add_section(section)

    assert builder.instance().section_count == 1
    assert builder.instance().first_section is section


def test_add_sections_adds_all_sections():
    builder = DocumentBuilder()

    sections = [
        make_section("section-1"),
        make_section("section-2"),
        make_section("section-3"),
    ]

    result = builder.add_sections(sections)

    assert result is builder
    assert builder.instance().section_count == 3
    assert list(builder.instance().sections) == sections


# ============================================================
# Build
# ============================================================


def test_build_returns_document():
    builder = (
        DocumentBuilder()
        .with_title("Adi Parva")
        .with_document_type("Parva")
    )

    document = builder.build()

    assert isinstance(document, Document)
    assert document.metadata.title == "Adi Parva"
    assert (
        document.metadata.document_type
        == "Parva"
    )


def test_build_returns_independent_copy():
    builder = DocumentBuilder().with_title(
        "Adi Parva"
    )

    built = builder.build()

    builder.with_title("Bala Kanda")

    assert built.metadata.title == "Adi Parva"
    assert (
        builder.instance().metadata.title
        == "Bala Kanda"
    )


# ============================================================
# Reset / Reuse
# ============================================================


def test_reset_creates_fresh_document():
    builder = DocumentBuilder().with_title(
        "Adi Parva"
    )

    old_instance = builder.instance()

    result = builder.reset()

    assert result is builder
    assert builder.instance() is not old_instance
    assert isinstance(builder.instance(), Document)


def test_reset_clears_metadata():
    builder = DocumentBuilder().with_title(
        "Adi Parva"
    )

    builder.add_author("Author")
    builder.reset()

    metadata = builder.instance().metadata

    assert metadata.title == ""
    assert metadata.authors == []


# ============================================================
# from_document
# ============================================================


def test_from_document_returns_document_builder():
    document = (
        DocumentBuilder()
        .with_title("Adi Parva")
        .build()
    )

    builder = DocumentBuilder.from_document(
        document
    )

    assert isinstance(
        builder,
        DocumentBuilder,
    )


def test_from_document_copies_metadata():
    document = (
        DocumentBuilder()
        .with_title("Adi Parva")
        .with_description("Description")
        .with_document_type("Parva")
        .with_publisher("Publisher")
        .with_edition("Edition")
        .with_publication_year("2026")
        .add_author("Author")
        .add_editor("Editor")
        .add_translator("Translator")
        .build()
    )

    builder = DocumentBuilder.from_document(
        document
    )

    metadata = builder.instance().metadata

    assert metadata.title == "Adi Parva"
    assert metadata.description == "Description"
    assert metadata.document_type == "Parva"
    assert metadata.publisher == "Publisher"
    assert metadata.edition == "Edition"
    assert metadata.publication_year == "2026"
    assert metadata.authors == ["Author"]
    assert metadata.editors == ["Editor"]
    assert metadata.translators == ["Translator"]


def test_from_document_copies_sections():
    section = make_section("section-1")

    document = (
        DocumentBuilder()
        .with_title("Adi Parva")
        .add_section(section)
        .build()
    )

    builder = DocumentBuilder.from_document(
        document
    )

    assert builder.instance().section_count == 1
    assert (
        builder.instance().first_section.id
        == section.id
    )


def test_from_document_does_not_alias_original():
    document = (
        DocumentBuilder()
        .with_title("Adi Parva")
        .build()
    )

    builder = DocumentBuilder.from_document(
        document
    )

    builder.with_title("Bala Kanda")

    assert document.metadata.title == "Adi Parva"
    assert (
        builder.instance().metadata.title
        == "Bala Kanda"
    )
