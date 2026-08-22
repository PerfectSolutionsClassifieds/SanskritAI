
from SanskritAI.acquisition.models.source_format import SourceFormat


def test_source_format_values():
    assert SourceFormat.TEXT.value == "text"
    assert SourceFormat.TXT.value == "txt"
    assert SourceFormat.XML.value == "xml"
    assert SourceFormat.TEI_XML.value == "tei_xml"
    assert SourceFormat.JSON.value == "json"
    assert SourceFormat.PDF.value == "pdf"
    assert SourceFormat.EPUB.value == "epub"
    assert SourceFormat.UNKNOWN.value == "unknown"


def test_text_formats():
    assert SourceFormat.TEXT.is_text
    assert SourceFormat.TXT.is_text
    assert SourceFormat.XML.is_text
    assert SourceFormat.TEI_XML.is_text
    assert SourceFormat.JSON.is_text
    assert SourceFormat.YAML.is_text
    assert SourceFormat.CSV.is_text
    assert SourceFormat.TSV.is_text
    assert SourceFormat.MARKDOWN.is_text
    assert SourceFormat.HTML.is_text

    assert not SourceFormat.PDF.is_text
    assert not SourceFormat.ZIP.is_text


def test_structured_formats():
    for source_format in (
        SourceFormat.XML,
        SourceFormat.TEI_XML,
        SourceFormat.JSON,
        SourceFormat.YAML,
        SourceFormat.CSV,
        SourceFormat.TSV,
        SourceFormat.SQLITE,
        SourceFormat.SQL,
        SourceFormat.XLSX,
    ):
        assert source_format.is_structured

    assert not SourceFormat.TXT.is_structured
    assert not SourceFormat.PDF.is_structured


def test_archive_formats():
    assert SourceFormat.ZIP.is_archive
    assert SourceFormat.TAR.is_archive
    assert SourceFormat.GZIP.is_archive

    assert not SourceFormat.PDF.is_archive
    assert not SourceFormat.XML.is_archive


def test_ocr_formats():
    assert SourceFormat.IMAGE.requires_ocr
    assert SourceFormat.JPEG.requires_ocr
    assert SourceFormat.PNG.requires_ocr
    assert SourceFormat.TIFF.requires_ocr

    assert not SourceFormat.PDF.requires_ocr
    assert not SourceFormat.TXT.requires_ocr


def test_document_formats():
    assert SourceFormat.PDF.is_document
    assert SourceFormat.EPUB.is_document

    assert not SourceFormat.TXT.is_document
    assert not SourceFormat.XML.is_document


def test_from_extension_normalizes_input():
    assert SourceFormat.from_extension(".xml") is SourceFormat.XML
    assert SourceFormat.from_extension("XML") is SourceFormat.XML
    assert SourceFormat.from_extension(".YML") is SourceFormat.YAML
    assert SourceFormat.from_extension(".db") is SourceFormat.SQLITE
    assert SourceFormat.from_extension(".gzip") is SourceFormat.GZIP
    assert SourceFormat.from_extension(".jpeg") is SourceFormat.JPEG
    assert SourceFormat.from_extension(".tif") is SourceFormat.TIFF


def test_from_extension_unknown_returns_unknown():
    assert (
        SourceFormat.from_extension(".something")
        is SourceFormat.UNKNOWN
    )


def test_string_representation():
    assert str(SourceFormat.XML) == "xml"
    assert str(SourceFormat.PDF) == "pdf"
