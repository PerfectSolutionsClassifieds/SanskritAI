
import pytest

from SanskritAI.acquisition.knowledge.pipelines.abstract_lexical_pipeline import (
    AbstractLexicalPipeline,
)


# ============================================================
# Test Doubles
# ============================================================

class DummyConnector:

    def __init__(self, events):
        self.events = events

    def connect(self):
        self.events.append("connect")

    def fetch(self):
        self.events.append("fetch")
        return "raw-resource"


class DummyParser:

    def __init__(self, events):
        self.events = events

    def parse(self, resource):
        self.events.append(("parse", resource))
        return ["raw-entry"]


class DummyTransformer:

    def __init__(self, events):
        self.events = events

    def transform(self, raw_entries):
        self.events.append(("transform", raw_entries))
        return ["canonical-entry"]


class DummyRepository:

    def __init__(self, events):
        self.events = events

    def store(self, records):
        self.events.append(("persist", records))
        return ["persisted-entry"]


class ConcretePipeline(AbstractLexicalPipeline):

    def __init__(self, events):
        super().__init__(
            connector=DummyConnector(events),
            parser=DummyParser(events),
            transformer=DummyTransformer(events),
            repository=DummyRepository(events),
        )
        self.events = events

    def before_pipeline(self):
        self.events.append("before")

    def after_pipeline(self):
        self.events.append("after")

    def build_manifest(self, persisted_objects):
        self.events.append(("manifest", persisted_objects))
        return {
            "total": len(persisted_objects),
        }


# ============================================================
# Abstract Contract
# ============================================================

def test_abstract_pipeline_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AbstractLexicalPipeline(
            connector=None,
            parser=None,
            transformer=None,
            repository=None,
        )


# ============================================================
# Stage Delegation
# ============================================================

def test_connect_delegates_to_connector():
    events = []
    pipeline = ConcretePipeline(events)

    pipeline.connect()

    assert events == ["connect"]


def test_fetch_delegates_to_connector():
    events = []
    pipeline = ConcretePipeline(events)

    result = pipeline.fetch()

    assert result == "raw-resource"
    assert events == ["fetch"]


def test_parse_delegates_to_parser():
    events = []
    pipeline = ConcretePipeline(events)

    result = pipeline.parse("resource")

    assert result == ["raw-entry"]
    assert events == [("parse", "resource")]


def test_transform_delegates_to_transformer():
    events = []
    pipeline = ConcretePipeline(events)

    result = pipeline.transform(["raw"])

    assert result == ["canonical-entry"]
    assert events == [("transform", ["raw"])]


def test_validate_returns_records_unchanged():
    events = []
    pipeline = ConcretePipeline(events)

    records = ["canonical"]

    assert pipeline.validate(records) is records


def test_persist_delegates_to_repository():
    events = []
    pipeline = ConcretePipeline(events)

    result = pipeline.persist(["canonical"])

    assert result == ["persisted-entry"]
    assert events == [("persist", ["canonical"])]


# ============================================================
# Complete Lifecycle
# ============================================================

def test_execute_runs_complete_pipeline_in_order():
    events = []

    pipeline = ConcretePipeline(events)

    result = pipeline.execute()

    assert events == [
        "before",
        "connect",
        "fetch",
        ("parse", "raw-resource"),
        ("transform", ["raw-entry"]),
        ("persist", ["canonical-entry"]),
        ("manifest", ["persisted-entry"]),
        "after",
    ]

    assert result == {
        "pipeline": "ConcretePipeline",
        "manifest": {
            "total": 1,
        },
    }


def test_execute_assigns_manifest():
    events = []

    pipeline = ConcretePipeline(events)

    pipeline.execute()

    assert pipeline.manifest == {
        "total": 1,
    }


# ============================================================
# Report
# ============================================================

def test_report_returns_pipeline_and_manifest():
    events = []

    pipeline = ConcretePipeline(events)

    pipeline.manifest = {"total": 5}

    assert pipeline.report() == {
        "pipeline": "ConcretePipeline",
        "manifest": {"total": 5},
    }


# ============================================================
# Summary
# ============================================================

def test_summary_identifies_pipeline_components():
    events = []

    pipeline = ConcretePipeline(events)

    summary = pipeline.summary()

    assert summary == {
        "pipeline": "ConcretePipeline",
        "connector": "DummyConnector",
        "parser": "DummyParser",
        "transformer": "DummyTransformer",
        "repository": "DummyRepository",
    }


# ============================================================
# String Representation
# ============================================================

def test_string_representation():
    events = []

    pipeline = ConcretePipeline(events)

    text = str(pipeline)

    assert text == "ConcretePipeline(DummyConnector)"
