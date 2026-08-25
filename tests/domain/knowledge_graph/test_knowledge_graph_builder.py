
from SanskritAI.domain.knowledge_graph.knowledge_graph import (
    KnowledgeGraph,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_builder import (
    KnowledgeGraphBuilder,
)


def test_builder_can_be_created():
    builder = KnowledgeGraphBuilder()

    assert builder is not None


def test_builder_is_displayable():
    builder = KnowledgeGraphBuilder()

    assert builder.is_displayable is True


def test_builder_display_name():
    builder = KnowledgeGraphBuilder()

    assert builder.display_name == "Knowledge Graph Builder"


def test_builder_display_text():
    builder = KnowledgeGraphBuilder()

    assert builder.display_text == "Knowledge Graph Builder"


def test_builder_display_description():
    builder = KnowledgeGraphBuilder()

    assert (
        builder.display_description
        == "Builds KnowledgeGraph instances from upstream outputs."
    )

# def test_builder_string_representation():
#     builder = KnowledgeGraphBuilder()

#     assert str(builder) == "Knowledge Graph Builder"

def test_builder_string_representation():
    builder = KnowledgeGraphBuilder()

    assert str(builder) == "KnowledgeGraphBuilder()"

def test_builder_is_slot_based():
    builder = KnowledgeGraphBuilder()

    assert not hasattr(builder, "__dict__")


def test_builder_from_semantic_collection_empty():
    builder = KnowledgeGraphBuilder()

    graph = builder.from_semantic(
        "graph-1",
        [],
    )

    assert isinstance(graph, KnowledgeGraph)
    assert graph.identifier == "graph-1"
    assert graph.node_count == 0
    assert graph.edge_count == 0
    assert graph.metadata["source"] == "semantic"


def test_builder_from_chandas_empty():
    builder = KnowledgeGraphBuilder()

    graph = builder.from_chandas(
        "graph-1",
        [],
    )

    assert isinstance(graph, KnowledgeGraph)
    assert graph.identifier == "graph-1"
    assert graph.node_count == 0
    assert graph.edge_count == 0
    assert graph.metadata["source"] == "chandas"


def test_builder_from_alankara_empty():
    builder = KnowledgeGraphBuilder()

    graph = builder.from_alankara(
        "graph-1",
        [],
    )

    assert isinstance(graph, KnowledgeGraph)
    assert graph.identifier == "graph-1"
    assert graph.node_count == 0
    assert graph.edge_count == 0
    assert graph.metadata["source"] == "alankara"


def test_builder_from_derivation_empty():
    builder = KnowledgeGraphBuilder()

    graph = builder.from_derivation(
        "graph-1",
        [],
    )

    assert isinstance(graph, KnowledgeGraph)
    assert graph.identifier == "graph-1"
    assert graph.node_count == 0
    assert graph.edge_count == 0
    assert graph.metadata["source"] == "derivation"


def test_semantic_collection_creates_analysis_nodes():
    from types import SimpleNamespace

    builder = KnowledgeGraphBuilder()

    analysis = SimpleNamespace(
        display_name="रामः",
        display_description="Semantic analysis",
        text="रामः",
        meaning="Rama",
        semantic_type="entity",
        confidence=0.90,
    )

    graph = builder.from_semantic(
        "graph-1",
        [analysis],
    )

    assert graph.node_count == 1

    node = graph.nodes[0]

    assert node.identifier == "graph-1:semantic:1"
    assert node.label == "रामः"
    assert node.node_type == "semantic.analysis"
    assert node.description == "Semantic analysis"
    assert node.payload["text"] == "रामः"
    assert node.payload["meaning"] == "Rama"
    assert node.payload["semantic_type"] == "entity"
    assert node.confidence == 0.90


def test_chandas_collection_creates_nodes():
    from types import SimpleNamespace

    builder = KnowledgeGraphBuilder()

    analysis = SimpleNamespace(
        meter="Anuṣṭubh",
        display_description="Anuṣṭubh analysis",
        text="श्लोक",
        meter_class="classical",
        syllable_count=32,
        pada_count=4,
        confidence=0.95,
    )

    graph = builder.from_chandas(
        "graph-1",
        [analysis],
    )

    assert graph.node_count == 1

    node = graph.nodes[0]

    assert node.identifier == "graph-1:chandas:1"
    assert node.label == "Anuṣṭubh"
    assert node.node_type == "chandas.analysis"
    assert node.payload["meter"] == "Anuṣṭubh"
    assert node.payload["meter_class"] == "classical"
    assert node.payload["syllable_count"] == 32
    assert node.payload["pada_count"] == 4
    assert node.confidence == 0.95


def test_alankara_collection_creates_nodes():
    from types import SimpleNamespace

    builder = KnowledgeGraphBuilder()

    analysis = SimpleNamespace(
        alankara="Upamā",
        display_description="Alankara analysis",
        text="इव",
        alankara_class="arthalankara",
        confidence=0.88,
    )

    graph = builder.from_alankara(
        "graph-1",
        [analysis],
    )

    assert graph.node_count == 1

    node = graph.nodes[0]

    assert node.identifier == "graph-1:alankara:1"
    assert node.label == "Upamā"
    assert node.node_type == "alankara.analysis"
    assert node.payload["text"] == "इव"
    assert node.payload["alankara"] == "Upamā"
    assert node.payload["alankara_class"] == "arthalankara"
    assert node.confidence == 0.88


def test_semantic_analysis_identifiers_are_sequential():
    from types import SimpleNamespace

    builder = KnowledgeGraphBuilder()

    analyses = [
        SimpleNamespace(
            display_name="रामः",
            display_description="First",
            text="रामः",
            meaning="Rama",
            semantic_type="entity",
            confidence=0.9,
        ),
        SimpleNamespace(
            display_name="वनम्",
            display_description="Second",
            text="वनम्",
            meaning="forest",
            semantic_type="place",
            confidence=0.8,
        ),
    ]

    graph = builder.from_semantic(
        "graph-1",
        analyses,
    )

    assert graph.node_count == 2
    assert graph.nodes[0].identifier == "graph-1:semantic:1"
    assert graph.nodes[1].identifier == "graph-1:semantic:2"


def test_builder_preserves_confidence():
    from types import SimpleNamespace

    builder = KnowledgeGraphBuilder()

    analysis = SimpleNamespace(
        display_name="Concept",
        display_description="Description",
        text="text",
        meaning="meaning",
        semantic_type="type",
        confidence=0.37,
    )

    graph = builder.from_semantic(
        "graph-1",
        [analysis],
    )

    assert graph.nodes[0].confidence == 0.37
