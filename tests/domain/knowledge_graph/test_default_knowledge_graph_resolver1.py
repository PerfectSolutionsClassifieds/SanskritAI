
from SanskritAI.domain.knowledge_graph.default_knowledge_graph_resolver import (
    DefaultKnowledgeGraphResolver,
)
from SanskritAI.domain.knowledge_graph.default_knowledge_graph_strategy import (
    DefaultKnowledgeGraphStrategy,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_resolver import (
    KnowledgeGraphResolver,
)


def test_default_resolver_is_knowledge_graph_resolver():
    resolver = DefaultKnowledgeGraphResolver()

    assert isinstance(
        resolver,
        KnowledgeGraphResolver,
    )


def test_default_resolver_can_be_created():
    resolver = DefaultKnowledgeGraphResolver()

    assert resolver is not None


def test_default_resolver_uses_default_strategy():
    resolver = DefaultKnowledgeGraphResolver()

    assert isinstance(
        resolver.strategy,
        DefaultKnowledgeGraphStrategy,
    )


def test_default_resolver_analyze_returns_result():
    from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
        KnowledgeGraphContext,
    )

    resolver = DefaultKnowledgeGraphResolver()

    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="रामः",
    )

    result = resolver.analyze(context)

    assert isinstance(
        result,
        KnowledgeGraphResult,
    )


def test_default_resolver_preserves_context():
    from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
        KnowledgeGraphContext,
    )

    resolver = DefaultKnowledgeGraphResolver()

    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="रामः",
    )

    result = resolver.analyze(context)

    assert result.context == context


def test_default_resolver_display_name():
    resolver = DefaultKnowledgeGraphResolver()

    assert resolver.display_name == "Default Knowledge Graph Resolver"


def test_default_resolver_display_text():
    resolver = DefaultKnowledgeGraphResolver()

    assert resolver.display_text == "Default Knowledge Graph Resolver"


def test_default_resolver_display_description():
    resolver = DefaultKnowledgeGraphResolver()

    assert (
        resolver.display_description
        == "Default knowledge graph resolver."
    )
