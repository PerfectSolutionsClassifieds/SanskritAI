
from SanskritAI.domain.knowledge_graph.default_knowledge_graph_strategy import (
    DefaultKnowledgeGraphStrategy,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_strategy import (
    KnowledgeGraphStrategy,
)


def test_default_strategy_is_knowledge_graph_strategy():
    strategy = DefaultKnowledgeGraphStrategy()

    assert isinstance(
        strategy,
        KnowledgeGraphStrategy,
    )


def test_default_strategy_can_be_created():
    strategy = DefaultKnowledgeGraphStrategy()

    assert strategy is not None


def test_default_strategy_has_expected_display_name():
    strategy = DefaultKnowledgeGraphStrategy()

    assert strategy.display_name == "Default Knowledge Graph Strategy"


def test_default_strategy_has_expected_display_text():
    strategy = DefaultKnowledgeGraphStrategy()

    assert strategy.display_text == "Default Knowledge Graph Strategy"


def test_default_strategy_has_expected_description():
    strategy = DefaultKnowledgeGraphStrategy()

    assert (
        strategy.display_description
        == "Default knowledge graph analysis strategy."
    )


def test_default_strategy_analyze_returns_result():
    from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
        KnowledgeGraphContext,
    )

    strategy = DefaultKnowledgeGraphStrategy()

    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="रामः",
    )

    result = strategy.analyze(context)

    assert isinstance(
        result,
        KnowledgeGraphResult,
    )


def test_default_strategy_preserves_context():
    from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
        KnowledgeGraphContext,
    )

    strategy = DefaultKnowledgeGraphStrategy()

    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="रामः",
    )

    result = strategy.analyze(context)

    assert result.context == context


def test_default_strategy_result_is_not_none():
    from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
        KnowledgeGraphContext,
    )

    strategy = DefaultKnowledgeGraphStrategy()

    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="रामः",
    )

    result = strategy.analyze(context)

    assert result is not None
