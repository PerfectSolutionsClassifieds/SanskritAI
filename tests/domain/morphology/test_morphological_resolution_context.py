from __future__ import annotations

from unittest.mock import Mock

from SanskritAI.domain.morphology.morphological_context import (
    MorphologicalContext,
)

from SanskritAI.domain.morphology.morphological_resolution_context import (
    MorphologicalResolutionContext,
)

from SanskritAI.domain.lexical.word_form import WordForm

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


class TestMorphologicalResolutionContext:

    def _create_context(self):
        resolution_context = Mock(
            spec=ResolutionContext,
        )

        word_form = Mock(
            spec=WordForm,
        )

        word_form.display_text = "रामः"

        return MorphologicalResolutionContext(
            resolution_context=resolution_context,
            word_form=word_form,
        )

    def test_is_morphological_context(self):
        context = self._create_context()

        assert isinstance(
            context,
            MorphologicalContext,
        )

    def test_is_morphological_resolution_context(self):
        context = self._create_context()

        assert isinstance(
            context,
            MorphologicalResolutionContext,
        )

    def test_does_not_duplicate_state(self):
        context = self._create_context()

        assert context.lexical_result is None
        assert context.dhatu_result is None
        assert context.canonical_repository is None
        assert context.dhatu_repository is None
        assert context.notes == ""

    def test_display_name(self):
        context = self._create_context()

        assert (
            context.display_name
            == "Morphological Resolution Context"
        )

    def test_display_text(self):
        context = self._create_context()

        assert context.display_text == "रामः"

    def test_display_description(self):
        context = self._create_context()

        assert context.display_description == (
            "Canonical context supplied to the "
            "Morphological Resolution Kernel."
        )

    def test_string_representation(self):
        context = self._create_context()

        assert str(context) == context.display_text

    def test_is_immutable(self):
        context = self._create_context()

        try:
            context.notes = "changed"
        except Exception:
            pass
        else:
            raise AssertionError(
                "MorphologicalResolutionContext must be immutable."
            )
