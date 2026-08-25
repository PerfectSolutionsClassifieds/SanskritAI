from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)


def test_context_can_be_created():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="रामः वनं गच्छति",
    )

    assert context.identifier == "ctx-1"
    assert context.subject == "रामः वनं गच्छति"


def test_context_defaults():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
    )

    assert context.source == ""
    assert context.language == "Sanskrit"
    assert context.script == "Devanagari"
    assert context.metadata == {}


def test_context_accepts_metadata():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
        metadata={
            "purana": "Bhagavata",
            "chapter": 1,
        },
    )

    assert context.get("purana") == "Bhagavata"
    assert context.get("chapter") == 1


def test_context_get_supports_default():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
    )

    assert context.get("missing") is None
    assert context.get("missing", "default") == "default"


def test_context_display_name():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
    )

    assert context.display_name == "Knowledge Graph Context"


def test_context_display_text_uses_subject():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
    )

    assert context.display_text == "हरिः"
    assert str(context) == "हरिः"


def test_context_display_description():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
    )

    assert (
        context.display_description
        == "Canonical context for knowledge graph construction."
    )


def test_context_is_immutable():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
    )

    assert context.is_immutable is True

    try:
        context.identifier = "ctx-2"
    except (AttributeError, TypeError):
        pass
    else:
        raise AssertionError("Context must be immutable")


def test_context_is_slot_based():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
    )

    assert not hasattr(context, "__dict__")
