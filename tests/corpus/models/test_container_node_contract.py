
from __future__ import annotations

import pytest

from SanskritAI.corpus.models.container_node import ContainerNode
from SanskritAI.corpus.models.document import Document
from SanskritAI.corpus.models.document_metadata import DocumentMetadata
from SanskritAI.corpus.models.section import Section
from SanskritAI.corpus.models.section_metadata import SectionMetadata
from SanskritAI.corpus.models.verse import Verse
from SanskritAI.corpus.models.verse_metadata import VerseMetadata
from SanskritAI.corpus.models.paragraph import Paragraph
from SanskritAI.corpus.models.paragraph_metadata import ParagraphMetadata
from SanskritAI.corpus.models.line import Line
from SanskritAI.corpus.models.line_metadata import LineMetadata
from SanskritAI.corpus.models.token import Token
from SanskritAI.corpus.models.token_metadata import TokenMetadata


# ============================================================
# Structural Contract Configuration
# ============================================================

def make_document(identifier: str):
    return Document(
        identifier=identifier,
        metadata=DocumentMetadata(),
    )


def make_section(identifier: str):
    return Section(
        identifier=identifier,
        metadata=SectionMetadata(),
    )


def make_verse(identifier: str):
    return Verse(
        identifier=identifier,
        metadata=VerseMetadata(),
    )


def make_paragraph(identifier: str):
    return Paragraph(
        identifier=identifier,
        metadata=ParagraphMetadata(),
    )


def make_line(identifier: str):
    return Line(
        identifier=identifier,
        metadata=LineMetadata(),
    )


def make_token(identifier: str):
    return Token(
        identifier=identifier,
        metadata=TokenMetadata(
            text=identifier,
        ),
    )


CONTAINER_CONTRACTS = [
    pytest.param(
        Document,
        make_document,
        make_section,
        "sections",
        "add_section",
        "remove_section",
        "section_count",
        "first_section",
        "last_section",
        id="Document",
    ),
    pytest.param(
        Section,
        make_section,
        make_verse,
        "verses",
        "add_verse",
        "remove_verse",
        "verse_count",
        "first_verse",
        "last_verse",
        id="Section",
    ),
    pytest.param(
        Verse,
        make_verse,
        make_paragraph,
        "paragraphs",
        "add_paragraph",
        "remove_paragraph",
        "paragraph_count",
        "first_paragraph",
        "last_paragraph",
        id="Verse",
    ),
    pytest.param(
        Paragraph,
        make_paragraph,
        make_line,
        "lines",
        "add_line",
        "remove_line",
        "line_count",
        "first_line",
        "last_line",
        id="Paragraph",
    ),
    pytest.param(
        Line,
        make_line,
        make_token,
        "tokens",
        "add_token",
        "remove_token",
        "token_count",
        "first_token",
        "last_token",
        id="Line",
    ),
]


# ============================================================
# Contract: ContainerNode inheritance
# ============================================================

@pytest.mark.parametrize(
    (
        "node_class",
        "make_parent",
        "make_child",
        "children_property",
        "add_method",
        "remove_method",
        "count_property",
        "first_property",
        "last_property",
    ),
    CONTAINER_CONTRACTS,
)
def test_structural_nodes_are_container_nodes(
    node_class,
    make_parent,
    make_child,
    children_property,
    add_method,
    remove_method,
    count_property,
    first_property,
    last_property,
):
    node = make_parent("parent-1")

    assert isinstance(node, ContainerNode)


# ============================================================
# Contract: empty state
# ============================================================

@pytest.mark.parametrize(
    (
        "node_class",
        "make_parent",
        "make_child",
        "children_property",
        "add_method",
        "remove_method",
        "count_property",
        "first_property",
        "last_property",
    ),
    CONTAINER_CONTRACTS,
)
def test_container_starts_empty(
    node_class,
    make_parent,
    make_child,
    children_property,
    add_method,
    remove_method,
    count_property,
    first_property,
    last_property,
):
    node = make_parent("parent-1")

    children = getattr(node, children_property)

    assert children is node.children
    assert children == []
    assert getattr(node, count_property) == 0
    assert node.is_leaf is True
    assert getattr(node, first_property) is None
    assert getattr(node, last_property) is None
    assert len(node) == 0


# ============================================================
# Contract: add child
# ============================================================

@pytest.mark.parametrize(
    (
        "node_class",
        "make_parent",
        "make_child",
        "children_property",
        "add_method",
        "remove_method",
        "count_property",
        "first_property",
        "last_property",
    ),
    CONTAINER_CONTRACTS,
)
def test_container_adds_child(
    node_class,
    make_parent,
    make_child,
    children_property,
    add_method,
    remove_method,
    count_property,
    first_property,
    last_property,
):
    node = make_parent("parent-1")
    child = make_child("child-1")

    getattr(node, add_method)(child)

    assert getattr(node, children_property) == [child]
    assert getattr(node, count_property) == 1
    assert node.is_leaf is False
    assert getattr(node, first_property) is child
    assert getattr(node, last_property) is child
    assert node[0] is child


# ============================================================
# Contract: insertion order
# ============================================================

@pytest.mark.parametrize(
    (
        "node_class",
        "make_parent",
        "make_child",
        "children_property",
        "add_method",
        "remove_method",
        "count_property",
        "first_property",
        "last_property",
    ),
    CONTAINER_CONTRACTS,
)
def test_container_preserves_insertion_order(
    node_class,
    make_parent,
    make_child,
    children_property,
    add_method,
    remove_method,
    count_property,
    first_property,
    last_property,
):
    node = make_parent("parent-1")

    first = make_child("child-1")
    second = make_child("child-2")
    third = make_child("child-3")

    add = getattr(node, add_method)

    add(first)
    add(second)
    add(third)

    assert getattr(node, children_property) == [
        first,
        second,
        third,
    ]

    assert node[0] is first
    assert node[1] is second
    assert node[2] is third

    assert getattr(node, first_property) is first
    assert getattr(node, last_property) is third


# ============================================================
# Contract: iteration
# ============================================================

@pytest.mark.parametrize(
    (
        "node_class",
        "make_parent",
        "make_child",
        "children_property",
        "add_method",
        "remove_method",
        "count_property",
        "first_property",
        "last_property",
    ),
    CONTAINER_CONTRACTS,
)
def test_container_is_iterable(
    node_class,
    make_parent,
    make_child,
    children_property,
    add_method,
    remove_method,
    count_property,
    first_property,
    last_property,
):
    node = make_parent("parent-1")

    children = [
        make_child("child-1"),
        make_child("child-2"),
        make_child("child-3"),
    ]

    add = getattr(node, add_method)

    for child in children:
        add(child)

    assert list(node) == children


# ============================================================
# Contract: extend
# ============================================================

@pytest.mark.parametrize(
    (
        "node_class",
        "make_parent",
        "make_child",
        "children_property",
        "add_method",
        "remove_method",
        "count_property",
        "first_property",
        "last_property",
    ),
    CONTAINER_CONTRACTS,
)
def test_container_extend(
    node_class,
    make_parent,
    make_child,
    children_property,
    add_method,
    remove_method,
    count_property,
    first_property,
    last_property,
):
    node = make_parent("parent-1")

    children = [
        make_child("child-1"),
        make_child("child-2"),
        make_child("child-3"),
    ]

    node.extend(children)

    assert getattr(node, children_property) == children
    assert getattr(node, count_property) == 3
    assert getattr(node, first_property) is children[0]
    assert getattr(node, last_property) is children[-1]


# ============================================================
# Contract: remove child
# ============================================================

@pytest.mark.parametrize(
    (
        "node_class",
        "make_parent",
        "make_child",
        "children_property",
        "add_method",
        "remove_method",
        "count_property",
        "first_property",
        "last_property",
    ),
    CONTAINER_CONTRACTS,
)
def test_container_remove_child(
    node_class,
    make_parent,
    make_child,
    children_property,
    add_method,
    remove_method,
    count_property,
    first_property,
    last_property,
):
    node = make_parent("parent-1")

    first = make_child("child-1")
    second = make_child("child-2")

    add = getattr(node, add_method)
    remove = getattr(node, remove_method)

    add(first)
    add(second)

    remove(first)

    assert getattr(node, children_property) == [second]
    assert getattr(node, count_property) == 1
    assert getattr(node, first_property) is second
    assert getattr(node, last_property) is second


# ============================================================
# Contract: clear children
# ============================================================

@pytest.mark.parametrize(
    (
        "node_class",
        "make_parent",
        "make_child",
        "children_property",
        "add_method",
        "remove_method",
        "count_property",
        "first_property",
        "last_property",
    ),
    CONTAINER_CONTRACTS,
)
def test_container_clear_children(
    node_class,
    make_parent,
    make_child,
    children_property,
    add_method,
    remove_method,
    count_property,
    first_property,
    last_property,
):
    node = make_parent("parent-1")

    add = getattr(node, add_method)

    add(make_child("child-1"))
    add(make_child("child-2"))

    node.clear_children()

    assert getattr(node, children_property) == []
    assert getattr(node, count_property) == 0
    assert node.is_leaf is True
    assert getattr(node, first_property) is None
    assert getattr(node, last_property) is None
    assert len(node) == 0


# ============================================================
# Contract: children alias is the canonical collection
# ============================================================

@pytest.mark.parametrize(
    (
        "node_class",
        "make_parent",
        "make_child",
        "children_property",
        "add_method",
        "remove_method",
        "count_property",
        "first_property",
        "last_property",
    ),
    CONTAINER_CONTRACTS,
)
def test_domain_children_alias_is_same_collection(
    node_class,
    make_parent,
    make_child,
    children_property,
    add_method,
    remove_method,
    count_property,
    first_property,
    last_property,
):
    node = make_parent("parent-1")

    domain_children = getattr(node, children_property)

    assert domain_children is node.children
