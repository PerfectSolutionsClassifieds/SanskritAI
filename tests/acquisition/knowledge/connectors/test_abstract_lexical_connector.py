
from pathlib import Path

import pytest

from SanskritAI.acquisition.knowledge.connectors.abstract_lexical_connector import (
    AbstractLexicalConnector,
)


# ============================================================
# Test Double
# ============================================================

class ConcreteLexicalConnector(AbstractLexicalConnector):
    """
    Minimal concrete implementation used only for testing
    AbstractLexicalConnector behavior.
    """

    def __init__(self):
        super().__init__(
            source_name="TestSource",
            source_version="1.0.0",
        )

        self.discover_called = False
        self.acquire_called = False
        self.parse_called = False
        self.transform_called = False
        self.publish_called = False

    # --------------------------------------------------------
    # Discovery
    # --------------------------------------------------------

    def discover(self):
        self.discover_called = True

        return {
            "source": self.source_name,
            "version": self.source_version,
        }

    # --------------------------------------------------------
    # Acquisition
    # --------------------------------------------------------

    def acquire(self, destination: Path) -> Path:
        self.acquire_called = True

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        source = destination / "test_source.txt"

        source.write_text(
            "hariḥ test",
            encoding="utf-8",
        )

        return source

    # --------------------------------------------------------
    # Parsing
    # --------------------------------------------------------

    def parse(self, source: Path):
        self.parse_called = True

        return {
            "source": source,
            "records": ["hariḥ test"],
        }

    # --------------------------------------------------------
    # Transformation
    # --------------------------------------------------------

    def transform(self, parsed):
        self.transform_called = True

        return {
            "records": parsed["records"],
            "canonical": True,
        }

    # --------------------------------------------------------
    # Publishing
    # --------------------------------------------------------

    def publish(self, transformed):
        self.publish_called = True

        return {
            "published": True,
            "records": transformed["records"],
        }


# ============================================================
# Construction
# ============================================================

def test_connector_can_be_instantiated_through_concrete_subclass():

    connector = ConcreteLexicalConnector()

    assert connector.source_name == "TestSource"
    assert connector.source_version == "1.0.0"


# ============================================================
# Abstract Contract
# ============================================================

def test_abstract_connector_cannot_be_instantiated_directly():

    with pytest.raises(TypeError):

        AbstractLexicalConnector(
            source_name="TestSource",
        )


# ============================================================
# Validation
# ============================================================

def test_validate_returns_transformed_object_unchanged():

    connector = ConcreteLexicalConnector()

    transformed = {
        "canonical": True,
    }

    result = connector.validate(
        transformed,
    )

    assert result is transformed


# ============================================================
# Summary
# ============================================================

def test_summary_returns_connector_metadata():

    connector = ConcreteLexicalConnector()

    summary = connector.summary()

    assert summary == {
        "source_name": "TestSource",
        "source_version": "1.0.0",
        "connector": "ConcreteLexicalConnector",
    }


# ============================================================
# String Representation
# ============================================================

def test_string_representation():

    connector = ConcreteLexicalConnector()

    text = str(connector)

    assert text == (
        "ConcreteLexicalConnector("
        "source='TestSource', "
        "version='1.0.0')"
    )


# ============================================================
# Individual Lifecycle Stages
# ============================================================

def test_discover_stage():

    connector = ConcreteLexicalConnector()

    result = connector.discover()

    assert connector.discover_called is True

    assert result == {
        "source": "TestSource",
        "version": "1.0.0",
    }


def test_acquire_stage(tmp_path):

    connector = ConcreteLexicalConnector()

    source = connector.acquire(
        tmp_path,
    )

    assert connector.acquire_called is True

    assert isinstance(
        source,
        Path,
    )

    assert source.exists()

    assert source.read_text(
        encoding="utf-8",
    ) == "hariḥ test"


def test_parse_stage(tmp_path):

    connector = ConcreteLexicalConnector()

    source = tmp_path / "source.txt"

    source.write_text(
        "hariḥ test",
        encoding="utf-8",
    )

    result = connector.parse(
        source,
    )

    assert connector.parse_called is True

    assert result["records"] == [
        "hariḥ test",
    ]


def test_transform_stage():

    connector = ConcreteLexicalConnector()

    parsed = {
        "records": [
            "hariḥ test",
        ],
    }

    result = connector.transform(
        parsed,
    )

    assert connector.transform_called is True

    assert result == {
        "records": [
            "hariḥ test",
        ],
        "canonical": True,
    }


def test_publish_stage():

    connector = ConcreteLexicalConnector()

    transformed = {
        "records": [
            "hariḥ test",
        ],
        "canonical": True,
    }

    result = connector.publish(
        transformed,
    )

    assert connector.publish_called is True

    assert result == {
        "published": True,
        "records": [
            "hariḥ test",
        ],
    }


# ============================================================
# Complete Execution Pipeline
# ============================================================

def test_execute_runs_complete_connector_lifecycle(tmp_path):

    connector = ConcreteLexicalConnector()

    result = connector.execute(
        tmp_path,
    )

    assert result == {
        "published": True,
        "records": [
            "hariḥ test",
        ],
    }

    assert connector.discover_called is True
    assert connector.acquire_called is True
    assert connector.parse_called is True
    assert connector.transform_called is True
    assert connector.publish_called is True


# ============================================================
# Lifecycle Ordering
# ============================================================

def test_execute_runs_stages_in_canonical_order(tmp_path):

    events = []

    class OrderedConnector(
        AbstractLexicalConnector,
    ):

        def __init__(self):

            super().__init__(
                source_name="OrderedSource",
                source_version="1.0.0",
            )

        def discover(self):

            events.append("discover")

            return {
                "discovered": True,
            }

        def acquire(self, destination):

            events.append("acquire")

            destination.mkdir(
                parents=True,
                exist_ok=True,
            )

            source = destination / "source.txt"

            source.write_text(
                "test",
                encoding="utf-8",
            )

            return source

        def parse(self, source):

            events.append("parse")

            return {
                "parsed": True,
            }

        def transform(self, parsed):

            events.append("transform")

            return {
                "transformed": True,
            }

        def validate(self, transformed):

            events.append("validate")

            return transformed

        def publish(self, transformed):

            events.append("publish")

            return {
                "published": True,
            }

    connector = OrderedConnector()

    connector.execute(
        tmp_path,
    )

    assert events == [
        "discover",
        "acquire",
        "parse",
        "transform",
        "validate",
        "publish",
    ]
