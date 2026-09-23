
from pathlib import Path

import pytest

from SanskritAI.acquisition.knowledge.connectors.abstract_lexical_connector import (
    AbstractLexicalConnector,
)


# ============================================================
# Test Double
# ============================================================

class ConcreteLexicalConnector(AbstractLexicalConnector):
    """Concrete test implementation of AbstractLexicalConnector."""

    def __init__(self, events):
        super().__init__(
            source_name="Test Source",
            source_version="1.0.0",
        )
        self.events = events

    def discover(self):
        self.events.append("discover")
        return {"source": self.source_name}

    def acquire(self, destination: Path) -> Path:
        self.events.append("acquire")
        return destination / "raw.txt"

    def parse(self, source: Path):
        self.events.append("parse")
        return ["raw-entry"]

    def transform(self, parsed):
        self.events.append("transform")
        return ["canonical-entry"]

    def publish(self, transformed):
        self.events.append("publish")
        return {"published": transformed}


# ============================================================
# Construction
# ============================================================

def test_connector_can_be_instantiated_through_concrete_subclass():
    connector = ConcreteLexicalConnector([])

    assert connector.source_name == "Test Source"
    assert connector.source_version == "1.0.0"


# ============================================================
# Abstract Contract
# ============================================================

def test_abstract_connector_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        AbstractLexicalConnector(source_name="Test")


# ============================================================
# Validation
# ============================================================

def test_validate_returns_transformed_object_unchanged():
    connector = ConcreteLexicalConnector([])

    value = {"canonical": True}

    assert connector.validate(value) is value


# ============================================================
# Execute
# ============================================================

def test_execute_runs_complete_acquisition_lifecycle(tmp_path):
    events = []

    connector = ConcreteLexicalConnector(events)

    result = connector.execute(tmp_path)

    assert events == [
        "discover",
        "acquire",
        "parse",
        "transform",
        "publish",
    ]

    assert result == {
        "published": ["canonical-entry"],
    }


def test_execute_passes_acquired_source_to_parser(tmp_path):
    class TrackingConnector(ConcreteLexicalConnector):
        def __init__(self):
            super().__init__([])
            self.acquired_path = None
            self.parsed_source = None

        def acquire(self, destination):
            self.acquired_path = destination / "source.txt"
            return self.acquired_path

        def parse(self, source):
            self.parsed_source = source
            return ["entry"]

    connector = TrackingConnector()

    connector.execute(tmp_path)

    assert connector.parsed_source == connector.acquired_path


# ============================================================
# Summary
# ============================================================

def test_summary_contains_connector_metadata():
    connector = ConcreteLexicalConnector([])

    summary = connector.summary()

    assert summary == {
        "source_name": "Test Source",
        "source_version": "1.0.0",
        "connector": "ConcreteLexicalConnector",
    }


# ============================================================
# String Representation
# ============================================================

def test_string_representation_contains_source_metadata():
    connector = ConcreteLexicalConnector([])

    text = str(connector)

    assert "ConcreteLexicalConnector" in text
    assert "Test Source" in text
    assert "1.0.0" in text
