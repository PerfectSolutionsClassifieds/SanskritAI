from SanskritAI.domain.knowledge_graph.knowledge_graph_diagnostic import (
    KnowledgeGraphDiagnostic,
)


def test_diagnostic_can_be_created():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Node is missing",
    )

    assert diagnostic.code == "KG001"
    assert diagnostic.message == "Node is missing"


def test_diagnostic_defaults():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Informational message",
    )

    assert diagnostic.severity == "INFO"
    assert diagnostic.rule == ""
    assert diagnostic.location == ""


def test_info_diagnostic():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Information",
        severity="INFO",
    )

    assert diagnostic.is_info is True
    assert diagnostic.is_warning is False
    assert diagnostic.is_error is False


def test_warning_diagnostic():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG002",
        message="Potential problem",
        severity="WARNING",
    )

    assert diagnostic.is_info is False
    assert diagnostic.is_warning is True
    assert diagnostic.is_error is False


def test_error_diagnostic():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG003",
        message="Invalid graph",
        severity="ERROR",
    )

    assert diagnostic.is_info is False
    assert diagnostic.is_warning is False
    assert diagnostic.is_error is True


def test_severity_checks_are_case_insensitive():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Warning",
        severity="warning",
    )

    assert diagnostic.is_warning is True
    assert diagnostic.is_info is False
    assert diagnostic.is_error is False


def test_diagnostic_display_name():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Something happened",
        severity="WARNING",
    )

    assert diagnostic.display_name == "WARNING"


def test_diagnostic_display_text():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Something happened",
        severity="WARNING",
    )

    assert diagnostic.display_text == "[WARNING] Something happened"
    assert str(diagnostic) == "[WARNING] Something happened"


def test_diagnostic_display_description():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Something happened",
        severity="ERROR",
    )

    assert diagnostic.display_description == "KG001"


def test_diagnostic_is_immutable():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Something happened",
    )

    assert diagnostic.is_immutable is True

    try:
        diagnostic.message = "Changed"
    except (AttributeError, TypeError):
        pass
    else:
        raise AssertionError("Diagnostic must be immutable")


def test_diagnostic_is_slot_based():
    diagnostic = KnowledgeGraphDiagnostic(
        code="KG001",
        message="Something happened",
    )

    assert not hasattr(diagnostic, "__dict__")
