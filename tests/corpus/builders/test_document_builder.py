
from SanskritAI.corpus.builders.document_builder import DocumentBuilder
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.document_metadata import DocumentMetadata
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import SectionMetadata


def make_section(title="Adi Parva"):
    return (
        Section(
            identifier="section-1",
            metadata=SectionMetadata(title=title),
        )
    )


def test_create_instance_returns_document():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .build()
    )

    assert isinstance(document, Document)


def test_create_instance_initializes_metadata():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .build()
    )

    assert isinstance(document.metadata, DocumentMetadata)


def test_create_instance_generates_identifier():
    first = (
        DocumentBuilder()
        .with_title("First")
        .build()
    )

    second = (
        DocumentBuilder()
        .with_title("Second")
        .build()
    )

    assert first.id is not None
    assert second.id is not None
    assert first.id != second.id


def test_with_title_is_fluent():
    builder = DocumentBuilder()

    result = builder.with_title("Mahabharata")

    assert result is builder


def test_with_document_type_sets_metadata():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .with_document_type("Purana")
        .build()
    )

    assert document.metadata.document_type == "Purana"


def test_with_page_range_sets_metadata():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .with_page_range(10, 25)
        .build()
    )

    assert document.metadata.start_page == 10
    assert document.metadata.end_page == 25
    assert document.metadata.page_count == 16


def test_with_publisher_sets_metadata():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .with_publisher("Chaukhamba")
        .build()
    )

    assert document.metadata.publisher == "Chaukhamba"


def test_with_edition_sets_metadata():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .with_edition("Critical Edition")
        .build()
    )

    assert document.metadata.edition == "Critical Edition"


def test_with_publication_year_sets_metadata():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .with_publication_year("2026")
        .build()
    )

    assert document.metadata.publication_year == "2026"


def test_add_author():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .add_author("Vyasa")
        .build()
    )

    assert document.metadata.authors == ["Vyasa"]


def test_add_editor():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .add_editor("Editor")
        .build()
    )

    assert document.metadata.editors == ["Editor"]


def test_add_translator():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .add_translator("Translator")
        .build()
    )

    assert document.metadata.translators == ["Translator"]


def test_add_section():
    section = make_section()

    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .add_section(section)
        .build()
    )

    assert document.section_count == 1
    assert document.first_section == section


def test_add_sections_preserves_order():
    sections = [
        make_section("First"),
        make_section("Second"),
        make_section("Third"),
    ]

    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .add_sections(sections)
        .build()
    )

    assert list(document.sections) == sections


def test_build_returns_independent_copy():
    builder = (
        DocumentBuilder()
        .with_title("Original")
    )

    first = builder.build()

    builder.with_title("Modified")

    second = builder.build()

    assert first.metadata.title == "Original"
    assert second.metadata.title == "Modified"
    assert first is not second


def test_reset_creates_fresh_document():
    builder = (
        DocumentBuilder()
        .with_title("Original")
    )

    original = builder.build()

    result = builder.reset()

    assert result is builder

    fresh = (
        builder
        .with_title("Fresh")
        .build()
    )

    assert fresh.metadata.title == "Fresh"
    assert fresh.id != original.id


def test_from_document_returns_document_builder():
    document = (
        DocumentBuilder()
        .with_title("Mahabharata")
        .build()
    )

    builder = DocumentBuilder.from_document(document)

    assert isinstance(builder, DocumentBuilder)


def test_from_document_does_not_alias_original():
    document = (
        DocumentBuilder()
        .with_title("Original")
        .build()
    )

    builder = DocumentBuilder.from_document(document)

    builder.with_title("Modified")

    assert document.metadata.title == "Original"
    assert builder.build().metadata.title == "Modified"
