
from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


def make_context(**overrides):
    values = {
        "identifier": "ctx-1",
        "subject": "हरिः",
    }
    values.update(overrides)
    return ResolutionContext(**values)


def test_context_can_be_created_with_required_fields():
    context = make_context()

    assert context.identifier == "ctx-1"
    assert context.subject == "हरिः"


def test_context_defaults_are_empty():
    context = make_context()

    assert context.source == ""
    assert context.language == ""
    assert context.script == ""
    assert context.metadata is None


def test_context_preserves_optional_context():
    context = make_context(
        source="Mahabharata",
        language="Sanskrit",
        script="Devanagari",
        metadata={"chapter": 1},
    )

    assert context.source == "Mahabharata"
    assert context.language == "Sanskrit"
    assert context.script == "Devanagari"
    assert context.metadata == {"chapter": 1}


def test_display_properties():
    context = make_context()

    assert context.display_name == "Resolution Context"
    assert context.display_text == "हरिः"
    assert (
        context.display_description
        == "Immutable context supplied to a domain resolver."
    )


def test_subject_is_used_as_display_text():
    subject = object()
    context = make_context(subject=subject)

    assert context.display_text == str(subject)


def test_source_language_and_script_flags():
    context = make_context(
        source="source",
        language="Sanskrit",
        script="Devanagari",
    )

    assert context.has_source
    assert context.has_language
    assert context.has_script


def test_empty_source_language_and_script_flags_are_false():
    context = make_context()

    assert not context.has_source
    assert not context.has_language
    assert not context.has_script


def test_metadata_flag():
    empty = make_context()
    populated = make_context(metadata={"chapter": 1})

    assert not empty.has_metadata
    assert populated.has_metadata


def test_get_metadata_returns_value():
    context = make_context(
        metadata={"chapter": 1},
    )

    assert context.get_metadata("chapter") == 1


def test_get_metadata_returns_default_for_missing_key():
    context = make_context(
        metadata={"chapter": 1},
    )

    assert context.get_metadata(
        "missing",
        "default",
    ) == "default"


def test_get_metadata_returns_default_when_metadata_is_none():
    context = make_context()

    assert context.get_metadata(
        "missing",
        "default",
    ) == "default"


def test_context_is_immutable():
    context = make_context()

    with pytest.raises(FrozenInstanceError):
        context.identifier = "changed"


def test_context_is_slot_based():
    context = make_context()

    assert not hasattr(context, "__dict__")


def test_context_is_immutable_and_displayable():
    context = make_context()

    assert context.is_immutable is True
    assert context.is_displayable is True


def test_string_representation_uses_display_text():
    context = make_context()

    assert str(context) == "हरिः"
