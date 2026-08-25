
import pytest

from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_strategy import (
    KnowledgeGraphStrategy,
)


def test_strategy_is_abstract():
    with pytest.raises(TypeError):
        KnowledgeGraphStrategy()


def test_strategy_display_name_uses_class_name():
    class TestStrategy(KnowledgeGraphStrategy):
        def analyze(self, context):
            return KnowledgeGraphResult(
                context=context,
            )

    strategy = TestStrategy()

    assert strategy.display_name == "TestStrategy"


def test_strategy_display_text():
    class TestStrategy(KnowledgeGraphStrategy):
        def analyze(self, context):
            return KnowledgeGraphResult(
                context=context,
            )

    strategy = TestStrategy()

    assert strategy.display_text == "TestStrategy"


def test_strategy_display_description():
    class TestStrategy(KnowledgeGraphStrategy):
        def analyze(self, context):
            return KnowledgeGraphResult(
                context=context,
            )

    strategy = TestStrategy()

    assert (
        strategy.display_description
        == "Abstract knowledge graph strategy."
    )


def test_strategy_string_representation():
    class TestStrategy(KnowledgeGraphStrategy):
        def analyze(self, context):
            return KnowledgeGraphResult(
                context=context,
            )

    strategy = TestStrategy()

    assert str(strategy) == "TestStrategy"


def test_strategy_analyze_contract():
    class TestStrategy(KnowledgeGraphStrategy):
        def analyze(self, context):
            return KnowledgeGraphResult(
                context=context,
            )

    strategy = TestStrategy()

    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
    )

    result = strategy.analyze(context)

    assert isinstance(
        result,
        KnowledgeGraphResult,
    )

    assert result.context == context
