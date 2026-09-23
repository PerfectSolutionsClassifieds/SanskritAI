
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

# ----------------------------------------------------------------------

# Test Fixtures / Construction Helpers

# ----------------------------------------------------------------------

def make_token(
text: str,
position: int = 1,
):
"""
Build one canonical Token.
"""

return (
    TokenBuilder()
    .with_text(text)
    .with_position(position)
    .build()
)

def make_line(
number: int = 1,
tokens=None,
):
"""
Build one canonical Line with optional Tokens.
"""

builder = (
    LineBuilder()
    .with_line_number(number)
)

if tokens:
    builder.add_tokens(tokens)

return builder.build()

def make_paragraph(
number: int = 1,
lines=None,
):
"""
Build one canonical Paragraph with optional Lines.
"""

builder = (
    ParagraphBuilder()
    .with_paragraph_number(number)
)

if lines:
    builder.add_lines(lines)

return builder.build()

def make_verse(
number: str = "1",
paragraphs=None,
):
"""
Build one canonical Verse with optional Paragraphs.
"""

builder = (
    VerseBuilder()
    .with_verse_number(number)
)

if paragraphs:
    builder.add_paragraphs(paragraphs)

return builder.build()

def make_section(
title: str,
number: str = "1",
verses=None,
):
"""
Build one canonical Section with optional Verses.
"""

builder = (
    SectionBuilder()
    .with_title(title)
    .with_section_number(number)
)

if verses:
    builder.add_verses(verses)

return builder.build()

def make_document(
title: str,
sections=None,
):
"""
Build one canonical Document with optional Sections.
"""

builder = (
    DocumentBuilder()
    .with_title(title)
)

if sections:
    builder.add_sections(sections)

return builder.build()

def make_corpus(
title: str,
documents=None,
):
"""
Build one canonical Corpus with optional Documents.
"""

builder = (
    CorpusBuilder()
    .with_title(title)
)

if documents:
    builder.add_documents(documents)

return builder.build()

# ----------------------------------------------------------------------

# Stage 4 — Complete Hierarchy Construction

# ----------------------------------------------------------------------

def test_build_complete_canonical_hierarchy():
"""
Verify that all seven canonical levels can be composed:

    Corpus
        Document
            Section
                Verse
                    Paragraph
                        Line
                            Token
"""

token = make_token("धर्मः", 1)

line = make_line(
    number=1,
    tokens=[token],
)

paragraph = make_paragraph(
    number=1,
    lines=[line],
)

verse = make_verse(
    number="1",
    paragraphs=[paragraph],
)

section = make_section(
    title="Chapter 1",
    number="1",
    verses=[verse],
)

document = make_document(
    title="Bhagavad Gita",
    sections=[section],
)

corpus = make_corpus(
    title="Sanskrit Canonical Corpus",
    documents=[document],
)

# Root
assert isinstance(corpus, Corpus)
assert corpus.document_count == 1

# Document
document = corpus.documents[0]
assert isinstance(document, Document)
assert document.section_count == 1

# Section
section = document.sections[0]
assert isinstance(section, Section)
assert section.verse_count == 1

# Verse
verse = section.verses[0]
assert isinstance(verse, Verse)
assert verse.paragraph_count == 1

# Paragraph
paragraph = verse.paragraphs[0]
assert isinstance(paragraph, Paragraph)
assert paragraph.line_count == 1

# Line
line = paragraph.lines[0]
assert isinstance(line, Line)
assert line.token_count == 1

# Token
token = line.tokens[0]
assert isinstance(token, Token)
assert token.text == "धर्मः"

# ----------------------------------------------------------------------

# Metadata Propagation Through the Hierarchy

# ----------------------------------------------------------------------

def test_metadata_survives_complete_hierarchy_construction():
"""
Verify that metadata assigned at every builder level survives
composition into the final Corpus.
"""

token = make_token(
    "धर्मः",
    position=1,
)

line = make_line(
    number=3,
    tokens=[token],
)

paragraph = make_paragraph(
    number=2,
    lines=[line],
)

verse = make_verse(
    number="4",
    paragraphs=[paragraph],
)

section = make_section(
    title="Adhyaya 1",
    number="1",
    verses=[verse],
)

document = make_document(
    title="Mahabharata",
    sections=[section],
)

corpus = make_corpus(
    title="Mahabharata Corpus",
    documents=[document],
)

assert corpus.metadata.title == "Mahabharata Corpus"

document = corpus.documents[0]
assert document.metadata.title == "Mahabharata"

section = document.sections[0]
assert section.metadata.title == "Adhyaya 1"
assert section.metadata.numbering_scheme == "1"

verse = section.verses[0]
assert verse.metadata.verse_number == "4"

paragraph = verse.paragraphs[0]
assert paragraph.metadata.paragraph_number == 2

line = paragraph.lines[0]
assert line.metadata.line_number == 3

token = line.tokens[0]
assert token.metadata.text == "धर्मः"
assert token.metadata.position == 1

# ----------------------------------------------------------------------

# Ordering

# ----------------------------------------------------------------------

def test_complete_hierarchy_preserves_sibling_order():
"""
Verify sibling ordering at every container level.
"""

token_1 = make_token("रामः", 1)
token_2 = make_token("वनम्", 2)

line_1 = make_line(
    1,
    [token_1],
)

line_2 = make_line(
    2,
    [token_2],
)

paragraph_1 = make_paragraph(
    1,
    [line_1],
)

paragraph_2 = make_paragraph(
    2,
    [line_2],
)

verse_1 = make_verse(
    "1",
    [paragraph_1],
)

verse_2 = make_verse(
    "2",
    [paragraph_2],
)

section_1 = make_section(
    "Chapter 1",
    "1",
    [verse_1],
)

section_2 = make_section(
    "Chapter 2",
    "2",
    [verse_2],
)

document_1 = make_document(
    "Ramayana",
    [section_1],
)

document_2 = make_document(
    "Mahabharata",
    [section_2],
)

corpus = make_corpus(
    "Sanskrit Corpus",
    [document_1, document_2],
)

assert corpus.documents[0].metadata.title == "Ramayana"
assert corpus.documents[1].metadata.title == "Mahabharata"

assert corpus.documents[0].sections[0].metadata.title == "Chapter 1"
assert corpus.documents[1].sections[0].metadata.title == "Chapter 2"

assert (
    corpus.documents[0]
    .sections[0]
    .verses[0]
    .metadata.verse_number
    == "1"
)

assert (
    corpus.documents[1]
    .sections[0]
    .verses[0]
    .metadata.verse_number
    == "2"
)

# ----------------------------------------------------------------------

# Identifier Integrity

# ----------------------------------------------------------------------

def test_complete_hierarchy_has_distinct_identifiers():
"""
Every canonical node must retain its own generated identifier.
"""

token = make_token("रामः", 1)
line = make_line(1, [token])
paragraph = make_paragraph(1, [line])
verse = make_verse("1", [paragraph])
section = make_section("Chapter 1", "1", [verse])
document = make_document("Ramayana", [section])
corpus = make_corpus("Sanskrit Corpus", [document])

identifiers = [
    corpus.id,
    document.id,
    section.id,
    verse.id,
    paragraph.id,
    line.id,
    token.id,
]

assert all(identifier is not None for identifier in identifiers)
assert len(set(identifiers)) == len(identifiers)

# ----------------------------------------------------------------------

# Recursive Serialization

# ----------------------------------------------------------------------

def test_complete_hierarchy_serializes_recursively():
"""
Verify that the complete hierarchy can be serialized through
the root Corpus.to_dict() operation.
"""

token = make_token("रामः", 1)
line = make_line(1, [token])
paragraph = make_paragraph(1, [line])
verse = make_verse("1", [paragraph])
section = make_section("Chapter 1", "1", [verse])
document = make_document("Ramayana", [section])
corpus = make_corpus("Sanskrit Corpus", [document])

data = corpus.to_dict()

assert isinstance(data, dict)
assert "id" in data
assert "metadata" in data
assert "documents" in data

assert len(data["documents"]) == 1

document_data = data["documents"][0]

assert "metadata" in document_data
assert "sections" in document_data
assert len(document_data["sections"]) == 1

section_data = document_data["sections"][0]

assert "metadata" in section_data
assert "verses" in section_data
assert len(section_data["verses"]) == 1

verse_data = section_data["verses"][0]

assert "metadata" in verse_data
assert "paragraphs" in verse_data
assert len(verse_data["paragraphs"]) == 1

paragraph_data = verse_data["paragraphs"][0]

assert "metadata" in paragraph_data
assert "lines" in paragraph_data
assert len(paragraph_data["lines"]) == 1

line_data = paragraph_data["lines"][0]

assert "metadata" in line_data
assert "tokens" in line_data
assert len(line_data["tokens"]) == 1

# ----------------------------------------------------------------------

# Defensive Copy / Build Semantics

# ----------------------------------------------------------------------

def test_build_returns_independent_complete_hierarchy():
"""
Verify that CorpusBuilder.build() returns a defensive deep copy
of the entire hierarchy.
"""

token = make_token("रामः", 1)
line = make_line(1, [token])
paragraph = make_paragraph(1, [line])
verse = make_verse("1", [paragraph])
section = make_section("Chapter 1", "1", [verse])
document = make_document("Ramayana", [section])

builder = (
    CorpusBuilder()
    .with_title("Sanskrit Corpus")
    .add_document(document)
)

first = builder.build()

# Change the working builder after the first build.
builder.with_title("Modified Corpus")

second = builder.build()

assert first.metadata.title == "Sanskrit Corpus"
assert second.metadata.title == "Modified Corpus"

# Nested data must also remain independent.
first_token = (
    first.documents[0]
    .sections[0]
    .verses[0]
    .paragraphs[0]
    .lines[0]
    .tokens[0]
)

second_token = (
    second.documents[0]
    .sections[0]
    .verses[0]
    .paragraphs[0]
    .lines[0]
    .tokens[0]
)

second_token.metadata.text = "लक्ष्मणः"

assert first_token.metadata.text == "रामः"
assert second_token.metadata.text == "लक्ष्मणः"

# ----------------------------------------------------------------------

# Builder Reuse / Reset

# ----------------------------------------------------------------------

def test_corpus_builder_reset_clears_complete_hierarchy():
"""
Reset must replace the working Corpus with a fresh instance,
removing all previously attached documents.
"""

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

fresh = builder.build()

assert isinstance(fresh, Corpus)
assert fresh.id != original_id
assert fresh.document_count == 0

# ----------------------------------------------------------------------

# Existing Hierarchy Reconstruction

# ----------------------------------------------------------------------

def test_from_instance_reconstructs_complete_hierarchy_without_aliasing():
"""
BaseBuilder.from_instance() must defensively copy an existing
complete Corpus hierarchy.
"""

```
token = make_token("रामः", 1)
line = make_line(1, [token])
paragraph = make_paragraph(1, [line])
verse = make_verse("1", [paragraph])
section = make_section("Chapter 1", "1", [verse])
document = make_document("Ramayana", [section])
original = make_corpus("Sanskrit Corpus", [document])

builder = CorpusBuilder().from_instance(original)

copied = builder.build()

assert copied is not original
assert copied.id == original.id
assert copied.documents[0].id == original.documents[0].id

copied.documents[0].metadata.title = "Modified Document"

assert original.documents[0].metadata.title == "Ramayana"

# ----------------------------------------------------------------------

# Realistic Multi-Level Corpus Scenario

# ----------------------------------------------------------------------

def test_realistic_multi_document_corpus_structure():
"""
Build a small but realistic multi-document canonical corpus.

```
This intentionally exercises the complete builder chain rather
than any single builder in isolation.
"""

ramayana_verse_1 = make_verse(
    "1",
    [
        make_paragraph(
            1,
            [
                make_line(
                    1,
                    [
                        make_token("तपः", 1),
                        make_token("स्वाध्यायः", 2),
                    ],
                ),
                make_line(
                    2,
                    [
                        make_token("निरतं", 1),
                        make_token("तपस्वी", 2),
                    ],
                ),
            ],
        )
    ],
)

ramayana_verse_2 = make_verse(
    "2",
    [
        make_paragraph(
            1,
            [
                make_line(
                    1,
                    [
                        make_token("रामः", 1),
                        make_token("वनम्", 2),
                    ],
                )
            ],
        )
    ],
)

ramayana_section = make_section(
    "Bala Kanda",
    "1",
    [
        ramayana_verse_1,
        ramayana_verse_2,
    ],
)

ramayana = make_document(
    "Ramayana",
    [ramayana_section],
)

mahabharata_verse = make_verse(
    "1",
    [
        make_paragraph(
            1,
            [
                make_line(
                    1,
                    [
                        make_token("धर्मः", 1),
                        make_token("सर्वत्र", 2),
                    ],
                )
            ],
        )
    ],
)

mahabharata_section = make_section(
    "Adi Parva",
    "1",
    [mahabharata_verse],
)

mahabharata = make_document(
    "Mahabharata",
    [mahabharata_section],
)

corpus = make_corpus(
    "Sanskrit Itihasa Corpus",
    [
        ramayana,
        mahabharata,
    ],
)

assert corpus.document_count == 2

assert corpus.documents[0].metadata.title == "Ramayana"
assert corpus.documents[1].metadata.title == "Mahabharata"

assert corpus.documents[0].section_count == 1
assert corpus.documents[1].section_count == 1

ramayana_section = corpus.documents[0].sections[0]

assert ramayana_section.verse_count == 2

first_verse = ramayana_section.verses[0]

assert first_verse.paragraph_count == 1
assert first_verse.paragraphs[0].line_count == 2
assert first_verse.paragraphs[0].lines[0].token_count == 2

first_token = (
    first_verse
    .paragraphs[0]
    .lines[0]
    .tokens[0]
)

assert first_token.text == "तपः"

mahabharata_section = corpus.documents[1].sections[0]

assert mahabharata_section.verse_count == 1
assert (
    mahabharata_section
    .verses[0]
    .paragraphs[0]
    .lines[0]
    .tokens[0]
    .text
    == "धर्मः"
)

