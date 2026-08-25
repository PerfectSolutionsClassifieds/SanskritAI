from SanskritAI.domain.knowledge_graph.knowledge_graph import (
    KnowledgeGraph,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_diagnostic import (
    KnowledgeGraphDiagnostic,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)


def make_context():
    return KnowledgeGraphContext(
        identifier="ctx-1",
        subject="हरिः",
    )


def make_graph():
    return KnowledgeGraph(
        identifier="graph-1",
    )


def make_non_empty_graph():
    context_graph = KnowledgeGraph(
        identifier="graph-1",
    )

    from SanskritAI.domain.knowledge_graph.knowledge_graph_node import (
        KnowledgeGraphNode,
    )

    return context_graph.add_node(
        KnowledgeGraphNode(
            identifier="node-1",
            label="हरिः",
        )
    )


def test_result_can_be_created():
    context = make_context()

    result = KnowledgeGraphResult(
        context=context,
    )

    assert result.context == context


def test_result_defaults():
    result = KnowledgeGraphResult(
        context=make_context(),
    )

    assert result.graph.identifier == "empty"
    assert result.succeeded is True
    assert result.confidence == 1.0
    assert result.diagnostics == ()


def test_result_identifier_comes_from_context():
    result = KnowledgeGraphResult(
        context=make_context(),
    )

    assert result.identifier == "ctx-1"


def test_result_context_properties():
    context = KnowledgeGraphContext(
        identifier="ctx-1",
        subject="रामः",
        source="Bhagavata",
        language="Sanskrit",
        script="Devanagari",
    )

    result = KnowledgeGraphResult(
        context=context,
    )

    assert result.subject == "रामः"
    assert result.source == "Bhagavata"
    assert result.language == "Sanskrit"
    assert result.script == "Devanagari"


def test_empty_result_has_no_graph():
    result = KnowledgeGraphResult(
        context=make_context(),
    )

    assert result.has_graph is False
    assert result.node_count == 0
    assert result.edge_count == 0


def test_result_can_contain_graph():
    graph = make_non_empty_graph()

    result = KnowledgeGraphResult(
        context=make_context(),
        graph=graph,
    )

    assert result.has_graph is True
    assert result.node_count == 1
    assert result.edge_count == 0
    assert result.result == graph


def test_successful_result_with_graph_is_resolved():
    result = KnowledgeGraphResult(
        context=make_context(),
        graph=make_non_empty_graph(),
        succeeded=True,
    )

    assert result.resolved is True
    assert result.unresolved is False


def test_successful_empty_result_is_unresolved():
    result = KnowledgeGraphResult(
        context=make_context(),
        succeeded=True,
    )

    assert result.resolved is False
    assert result.unresolved is True


def test_failed_result_is_unresolved():
    result = KnowledgeGraphResult(
        context=make_context(),
        graph=make_non_empty_graph(),
        succeeded=False,
    )

    assert result.resolved is False
    assert result.unresolved is True


def test_result_without_diagnostics():
    result = KnowledgeGraphResult(
        context=make_context(),
    )

    assert result.has_diagnostics is False
    assert result.diagnostic_count == 0
    assert result.first_diagnostic is None


def test_result_with_diagnostics():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Something went wrong",
        severity="ERROR",
    )

    result = KnowledgeGraphResult(
        context=make_context(),
        succeeded=False,
        diagnostics=(diagnostic,),
    )

    assert result.has_diagnostics is True
    assert result.diagnostic_count == 1
    assert result.first_diagnostic == diagnostic


def test_multiple_diagnostics_preserve_order():
    first = KnowledgeGraphDiagnostic(
        code="KG001",
        message="First",
    )

    second = KnowledgeGraphDiagnostic(
        code="KG002",
        message="Second",
        severity="WARNING",
    )

    result = KnowledgeGraphResult(
        context=make_context(),
        diagnostics=(first, second),
    )

    assert result.diagnostic_count == 2
    assert result.first_diagnostic == first
    assert result.diagnostics == (
        first,
        second,
    )


def test_result_confidence():
    result = KnowledgeGraphResult(
        context=make_context(),
        confidence=0.95,
    )

    assert result.confidence == 0.95
    assert result.is_confident is True


def test_low_confidence_result():
    result = KnowledgeGraphResult(
        context=make_context(),
        confidence=0.79,
    )

    assert result.is_confident is False


def test_confidence_boundary():
    result = KnowledgeGraphResult(
        context=make_context(),
        confidence=0.80,
    )

    assert result.is_confident is True


def test_result_display_name():
    result = KnowledgeGraphResult(
        context=make_context(),
    )

    assert result.display_name == "Knowledge Graph Result"


def test_successful_result_display_text():
    result = KnowledgeGraphResult(
        context=make_context(),
        succeeded=True,
    )

    assert result.display_text == "Knowledge Graph Result [Succeeded]"


def test_failed_result_display_text():
    result = KnowledgeGraphResult(
        context=make_context(),
        succeeded=False,
    )

    assert result.display_text == "Knowledge Graph Result [Failed]"


def test_diagnostic_has_display_priority():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Graph construction failed",
        severity="ERROR",
    )

    result = KnowledgeGraphResult(
        context=make_context(),
        graph=make_non_empty_graph(),
        diagnostics=(diagnostic,),
    )

    assert result.display_description == "Graph construction failed"


def test_graph_has_display_priority_when_no_diagnostics():
    graph = make_non_empty_graph()

    result = KnowledgeGraphResult(
        context=make_context(),
        graph=graph,
        diagnostics=(),
    )

    assert result.display_description == graph.display_text


def test_empty_result_has_empty_display_description():
    result = KnowledgeGraphResult(
        context=make_context(),
    )

    assert result.display_description == ""


def test_result_is_slot_based():
    result = KnowledgeGraphResult(
        context=make_context(),
    )

    assert not hasattr(result, "__dict__")


def test_result_is_immutable():
    result = KnowledgeGraphResult(
        context=make_context(),
    )

    assert result.is_immutable is True

    try:
        result.succeeded = False
    except (AttributeError, TypeError):
        pass
    else:
        raise AssertionError("KnowledgeGraphResult must be immutable")
