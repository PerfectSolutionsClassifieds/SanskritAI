
from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_resolver import (
    KnowledgeGraphResolver,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_strategy import (
    KnowledgeGraphStrategy,
)


class StubKnowledgeGraphStrategy(KnowledgeGraphStrategy):

    def __init__(self):
        self.calls = []

    def analyze(self, context):
        self.calls.append(context)

        return KnowledgeGraphResult(
            context=context,
        )


def test_resolver_can_be_created():
    strategy = StubKnowledgeGraphStrategy()

    resolver = KnowledgeGraphResolver(
        strategy,
    )

    assert resolver is not None


def test_resolver_exposes_strategy():
    strategy = StubKnowledgeGraphStrategy()

    resolver = KnowledgeGraphResolver(
        strategy,
    )

    assert resolver.strategy is strategy


def test_resolver_delegates_analyze():
    strategy = StubKnowledgeGraphStrategy()

    resolver = KnowledgeGraphResolver(
        strategy,
    )

    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="रामः",
    )

    result = resolver.analyze(context)

    assert isinstance(
        result,
        KnowledgeGraphResult,
    )

    assert result.context == context


def test_resolver_passes_same_context_to_strategy():
    strategy = StubKnowledgeGraphStrategy()

    resolver = KnowledgeGraphResolver(
        strategy,
    )

    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="रामः",
    )

    resolver.analyze(context)

    assert strategy.calls == [context]


def test_resolver_display_name():
    strategy = StubKnowledgeGraphStrategy()

    resolver = KnowledgeGraphResolver(
        strategy,
    )

    assert resolver.display_name == "KnowledgeGraphResolver"


def test_resolver_display_text():
    strategy = StubKnowledgeGraphStrategy()

    resolver = KnowledgeGraphResolver(
        strategy,
    )

    assert resolver.display_text == "KnowledgeGraphResolver"


def test_resolver_display_description():
    strategy = StubKnowledgeGraphStrategy()

    resolver = KnowledgeGraphResolver(
        strategy,
    )

    assert (
        resolver.display_description
        == "Delegates knowledge graph construction to a strategy."
    )


def test_resolver_string_representation():
    strategy = StubKnowledgeGraphStrategy()

    resolver = KnowledgeGraphResolver(
        strategy,
    )

    assert str(resolver) == "KnowledgeGraphResolver"
