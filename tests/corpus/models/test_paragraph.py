
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.line_metadata import LineMetadata
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.paragraph_metadata import ParagraphMetadata


def make_paragraph(identifier="paragraph-1"):
    return Paragraph(
        identifier=identifier,
        metadata=ParagraphMetadata(),
    )


def make_line(identifier="line-1"):
    return Line(
        identifier=identifier,
        metadata=LineMetadata(),
    )


def test_paragraph_stores_identifier():
    paragraph = make_paragraph()

    assert paragraph.id == "paragraph-1"


def test_paragraph_stores_metadata():
    metadata = ParagraphMetadata()

    paragraph = Paragraph(
        identifier="paragraph-1",
        metadata=metadata,
    )

    assert paragraph.metadata is metadata


def test_paragraph_starts_without_lines():
    paragraph = make_paragraph()

    assert paragraph.lines == []
    assert paragraph.line_count == 0


def test_lines_alias_children():
    paragraph = make_paragraph()

    assert paragraph.lines is paragraph.children


def test_add_line():
    paragraph = make_paragraph()
    line = make_line()

    paragraph.add_line(line)

    assert paragraph.lines == [line]
    assert paragraph.line_count == 1


def test_remove_line():
    paragraph = make_paragraph()
    line = make_line()

    paragraph.add_line(line)
    paragraph.remove_line(line)

    assert paragraph.lines == []
    assert paragraph.line_count == 0


def test_first_line():
    paragraph = make_paragraph()

    first = make_line("line-1")
    second = make_line("line-2")

    paragraph.add_line(first)
    paragraph.add_line(second)

    assert paragraph.first_line is first


def test_last_line():
    paragraph = make_paragraph()

    first = make_line("line-1")
    second = make_line("line-2")

    paragraph.add_line(first)
    paragraph.add_line(second)

    assert paragraph.last_line is second


def test_lines_preserve_insertion_order():
    paragraph = make_paragraph()

    lines = [
        make_line("line-1"),
        make_line("line-2"),
        make_line("line-3"),
    ]

    for line in lines:
        paragraph.add_line(line)

    assert paragraph.lines == lines
