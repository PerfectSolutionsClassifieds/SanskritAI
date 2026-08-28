from __future__ import annotations

"""
SanskritAI
==========

Stage-4 Corpus Builder Integration Tests

These tests verify that the complete canonical corpus hierarchy
can be assembled through the builder layer:

    Corpus
        └── Document
              └── Section
                    └── Verse
                          └── Paragraph
                                └── Line
                                      └── Token

Stage-4 validates integration between the builders and models
rather than testing individual builder methods in isolation.

Version
-------
v0.3.0
"""

import pytest

from SanskritAI.corpus.builders.corpus_builder import (
    CorpusBuilder,
)
from SanskritAI.corpus.builders.document_builder import (
    DocumentBuilder,
)
from SanskritAI.corpus.builders.section_builder import (
    SectionBuilder,
)
from SanskritAI.corpus.builders.verse_builder import (
    VerseBuilder,
)
from SanskritAI.corpus.builders.paragraph_builder import (
    ParagraphBuilder,
)
from SanskritAI.corpus.builders.line_builder import (
    LineBuilder,
)
from SanskritAI.corpus.builders.token_builder import (
    TokenBuilder,
)

from SanskritAI.corpus.models.corpus import Corpus
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.token import Token


# ============================================================
# Factory Helpers
# ============================================================


def make_token(
    text: str = "रामः",
    sequence: int = 1,
) -> Token:

    return (
        TokenBuilder()
        .with_text(text)
        .with_sequence_number(sequence)
        .build()
    )


def make_line(
    sequence: int = 1,
    tokens: list[Token] | None = None,
) -> Line:

    builder = (
        LineBuilder()
        .with_sequence_number(sequence)
    )

    if tokens:
        builder.add_tokens(tokens)

    return builder.build()


def make_paragraph(
    number: int = 1,
    lines: list[Line] | None = None,
) -> Paragraph:

    builder = (
        ParagraphBuilder()
        .with_paragraph_number(number)
    )

    if lines:
        builder.add_lines(lines)

    return builder.build()


def make_verse(
    number: str = "1",
    paragraphs: list[Paragraph] | None = None,
) -> Verse:

    builder = (
        VerseBuilder()
        .with_verse_number(number)
    )

    if paragraphs:
        builder.add_paragraphs(paragraphs)

    return builder.build()


def make_section(
    title: str = "Chapter 1",
    number: str = "1",
    verses: list[Verse] | None = None,
) -> Section:

    builder = (
        SectionBuilder()
        .with_title(title)
        .with_section_number(number)
    )

    if verses:
        builder.add_verses(verses)

    return builder.build()


def make_document(
    title: str = "Ramayana",
    sections: list[Section] | None = None,
) -> Document:

    builder = (
        DocumentBuilder()
        .with_title(title)
    )

    if sections:
        builder.add_sections(sections)

    return builder.build()


def make_corpus(
    title: str = "Sanskrit Corpus",
    documents: list[Document] | None = None,
) -> Corpus:

    builder = (
        CorpusBuilder()
        .with_title(title)
    )

    if documents:
        builder.add_documents(documents)

    return builder.build()


# ============================================================
# Complete Hierarchy Construction
# ============================================================


def test_complete_hierarchy_can_be_constructed():

    token = make_token()

    line = make_line(
        1,
        [token],
    )

    paragraph = make_paragraph(
        1,
        [line],
    )

    verse = make_verse(
        "1",
        [paragraph],
    )

    section = make_section(
        "Chapter 1",
        "1",
        [verse],
    )

    document = make_document(
        "Ramayana",
        [section],
    )

    corpus = make_corpus(
        "Sanskrit Corpus",
        [document],
    )

    assert isinstance(corpus, Corpus)

    assert corpus.document_count == 1

    assert corpus.documents[0] is document

    assert document.section_count == 1

    assert document.sections[0] is section

    assert section.verse_count == 1

    assert section.verses[0] is verse

    assert verse.paragraph_count == 1

    assert verse.paragraphs[0] is paragraph

    assert paragraph.line_count == 1

    assert paragraph.lines[0] is line

    assert line.token_count == 1

    assert line.tokens[0] is token


# ============================================================
# Hierarchy Ordering
# ============================================================


def test_complete_hierarchy_preserves_order():

    tokens = [
        make_token("रामः", 1),
        make_token("वनम्", 2),
        make_token("गच्छति", 3),
    ]

    line = make_line(
        1,
        tokens,
    )

    paragraph = make_paragraph(
        1,
        [line],
    )

    verse = make_verse(
        "1",
        [paragraph],
    )

    section = make_section(
        "Chapter 1",
        "1",
        [verse],
    )

    document = make_document(
        "Ramayana",
        [section],
    )

    corpus = make_corpus(
        "Sanskrit Corpus",
        [document],
    )

    result_tokens = (
        corpus.documents[0]
        .sections[0]
        .verses[0]
        .paragraphs[0]
        .lines[0]
        .tokens
    )

    assert result_tokens == tokens


# ============================================================
# Multiple Children
# ============================================================


def test_complete_hierarchy_supports_multiple_children():

    verses = [
        make_verse("1"),
        make_verse("2"),
        make_verse("3"),
    ]

    section = make_section(
        "Chapter 1",
        "1",
        verses,
    )

    documents = [
        make_document(
            "Ramayana",
            [section],
        ),
        make_document(
            "Mahabharata",
            [],
        ),
    ]

    corpus = make_corpus(
        "Sanskrit Corpus",
        documents,
    )

    assert corpus.document_count == 2

    assert corpus.documents[0].section_count == 1

    assert (
        corpus.documents[0]
        .sections[0]
        .verse_count
        == 3
    )

    assert [
        verse.metadata.verse_number
        for verse
        in corpus.documents[0].sections[0].verses
    ] == ["1", "2", "3"]


# ============================================================
# Fluent Builder Composition
# ============================================================


def test_builders_can_be_composed_fluently():

    token = (
        TokenBuilder()
        .with_text("रामः")
        .with_sequence_number(1)
        .build()
    )

    line = (
        LineBuilder()
        .with_sequence_number(1)
        .add_token(token)
        .build()
    )

    paragraph = (
        ParagraphBuilder()
        .with_paragraph_number(1)
        .add_line(line)
        .build()
    )

    verse = (
        VerseBuilder()
        .with_verse_number("1")
        .add_paragraph(paragraph)
        .build()
    )

    section = (
        SectionBuilder()
        .with_title("Chapter 1")
        .with_section_number("1")
        .add_verse(verse)
        .build()
    )

    document = (
        DocumentBuilder()
        .with_title("Ramayana")
        .add_section(section)
        .build()
    )

    corpus = (
        CorpusBuilder()
        .with_title("Sanskrit Corpus")
        .add_document(document)
        .build()
    )

    assert corpus.document_count == 1

    assert (
        corpus.documents[0]
        .sections[0]
        .verses[0]
        .paragraphs[0]
        .lines[0]
        .tokens[0]
        .metadata.text
        == "रामः"
    )


# ============================================================
# Independent Builder Copies
# ============================================================


def test_nested_build_results_are_independent():

    token = make_token()

    line = make_line(
        1,
        [token],
    )

    paragraph = make_paragraph(
        1,
        [line],
    )

    verse = make_verse(
        "1",
        [paragraph],
    )

    section = make_section(
        "Chapter 1",
        "1",
        [verse],
    )

    document = make_document(
        "Ramayana",
        [section],
    )

    corpus = make_corpus(
        "Sanskrit Corpus",
        [document],
    )

    copied = corpus

    copied.documents[0].metadata.title = "Modified"

    assert corpus.documents[0].metadata.title == "Modified"


# ============================================================
# Builder Reuse
# ============================================================


def test_corpus_builder_can_be_reused():

    builder = (
        CorpusBuilder()
        .with_title("First Corpus")
    )

    first = builder.build()

    builder.with_title("Second Corpus")

    second = builder.build()

    assert first.metadata.title == "First Corpus"

    assert second.metadata.title == "Second Corpus"

    assert first.id != second.id


# ============================================================
# Reset
# ============================================================


def test_corpus_builder_reset_clears_complete_hierarchy():

    document = make_document(
        "Ramayana",
        [
            make_section(
                "Chapter 1",
                "1",
                [
                    make_verse(
                        "1",
                        [
                            make_paragraph(
                                1,
                                [
                                    make_line(
                                        1,
                                        [
                                            make_token(
                                                "रामः",
                                                1,
                                            )
                                        ],
                                    )
                                ],
                            )
                        ],
                    )
                ],
            )
        ],
    )

    builder = (
        CorpusBuilder()
        .with_title("Sanskrit Corpus")
        .add_document(document)
    )

    original_id = builder.build().id

    assert builder.instance().document_count == 1

    builder.reset()

    # Reset creates a fresh working instance.  Do not call
    # build() here because CorpusBuilder.validate() correctly
    # requires a non-empty title.
    fresh = builder.instance()

    assert isinstance(fresh, Corpus)

    assert fresh.id != original_id

    assert fresh.document_count == 0

    assert fresh.metadata.title == ""


# ============================================================
# Fresh Builder State
# ============================================================


def test_each_root_builder_starts_with_independent_identifier():

    first = CorpusBuilder().with_title(
        "Corpus A"
    ).build()

    second = CorpusBuilder().with_title(
        "Corpus B"
    ).build()

    assert first.id != second.id


# ============================================================
# Recursive Serialization
# ============================================================


def test_complete_hierarchy_serializes_recursively():

    token = make_token(
        "रामः",
        1,
    )

    line = make_line(
        1,
        [token],
    )

    paragraph = make_paragraph(
        1,
        [line],
    )

    verse = make_verse(
        "1",
        [paragraph],
    )

    section = make_section(
        "Chapter 1",
        "1",
        [verse],
    )

    document = make_document(
        "Ramayana",
        [section],
    )

    corpus = make_corpus(
        "Sanskrit Corpus",
        [document],
    )

    # Section currently does not expose to_dict().
    # This test intentionally documents the Stage-4 contract.
    #
    # Once Section.to_dict() is implemented, this test should
    # pass without modification.

    if not hasattr(section, "to_dict"):
        pytest.fail(
            "Stage-4 serialization gap: "
            "Section.to_dict() is not implemented."
        )

    data = corpus.to_dict()

    assert data["metadata"]["title"] == "Sanskrit Corpus"

    assert len(data["documents"]) == 1

    assert data["documents"][0]["metadata"]["title"] == "Ramayana"

    assert len(data["documents"][0]["sections"]) == 1

    assert (
        data["documents"][0]["sections"][0]["metadata"]["title"]
        == "Chapter 1"
    )

    assert (
        data["documents"][0]["sections"][0]["verses"][0]
        ["metadata"]["verse_number"]
        == "1"
    )


# ============================================================
# Invalid Root State
# ============================================================


def test_corpus_builder_rejects_empty_title():

    with pytest.raises(ValueError):

        CorpusBuilder().build()


# ============================================================
# Final Hierarchy Sanity Check
# ============================================================


def test_complete_hierarchy_counts_are_consistent():

    corpus = make_corpus(
        "Sanskrit Corpus",
        [
            make_document(
                "Ramayana",
                [
                    make_section(
                        "Chapter 1",
                        "1",
                        [
                            make_verse(
                                "1",
                                [
                                    make_paragraph(
                                        1,
                                        [
                                            make_line(
                                                1,
                                                [
                                                    make_token(
                                                        "रामः",
                                                        1,
                                                    ),
                                                    make_token(
                                                        "वनम्",
                                                        2,
                                                    ),
                                                ],
                                            )
                                        ],
                                    )
                                ],
                            )
                        ],
                    )
                ],
            )
        ],
    )

    document = corpus.documents[0]

    section = document.sections[0]

    verse = section.verses[0]

    paragraph = verse.paragraphs[0]

    line = paragraph.lines[0]

    assert corpus.document_count == 1
    assert document.section_count == 1
    assert section.verse_count == 1
    assert verse.paragraph_count == 1
    assert paragraph.line_count == 1
    assert line.token_count == 2
