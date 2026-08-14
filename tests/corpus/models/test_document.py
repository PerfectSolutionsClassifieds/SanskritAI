
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.document_metadata import DocumentMetadata
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import SectionMetadata


def make_document(identifier="document-1"):
    return Document(
        identifier=identifier,
        metadata=DocumentMetadata(),
    )


def make_section(identifier="section-1"):
    return Section(
        identifier=identifier,
        metadata=SectionMetadata(),
    )


def test_document_stores_identifier():
    document = make_document()

    assert document.id == "document-1"


def test_document_stores_metadata():
    metadata = DocumentMetadata()

    document = Document(
        identifier="document-1",
        metadata=metadata,
    )

    assert document.metadata is metadata


def test_document_starts_without_sections():
    document = make_document()

    assert document.sections == []
    assert document.section_count == 0


def test_sections_alias_children():
    document = make_document()

    assert document.sections is document.children


def test_add_section():
    document = make_document()
    section = make_section()

    document.add_section(section)

    assert document.sections == [section]
    assert document.section_count == 1


def test_remove_section():
    document = make_document()
    section = make_section()

    document.add_section(section)
    document.remove_section(section)

    assert document.sections == []
    assert document.section_count == 0


def test_first_section():
    document = make_document()
    first = make_section("section-1")
    second = make_section("section-2")

    document.add_section(first)
    document.add_section(second)

    assert document.first_section is first


def test_last_section():
    document = make_document()
    first = make_section("section-1")
    second = make_section("section-2")

    document.add_section(first)
    document.add_section(second)

    assert document.last_section is second


def test_sections_preserve_insertion_order():
    document = make_document()

    sections = [
        make_section("section-1"),
        make_section("section-2"),
        make_section("section-3"),
    ]

    for section in sections:
        document.add_section(section)

    assert document.sections == sections
