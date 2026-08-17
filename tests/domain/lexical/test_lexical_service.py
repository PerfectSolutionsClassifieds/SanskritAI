from __future__ import annotations

from unittest.mock import Mock

from SanskritAI.domain.lexical.lexical_lookup_engine import (
    LexicalLookupEngine,
)

from SanskritAI.domain.lexical.lexical_service import (
    LexicalService,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


class TestLexicalService:

    def _repository(self):
        return Mock()

    def _context(self):
        return ResolutionContext(
            identifier="test",
            subject="रामः",
        )

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def test_can_be_created(self):

        repository = self._repository()

        service = LexicalService(
            repository=repository,
        )

        assert service is not None
        assert service.repository is repository

    def test_is_frozen(self):

        repository = self._repository()

        service = LexicalService(
            repository=repository,
        )

        try:
            service.repository = Mock()
        except AttributeError:
            pass
        else:
            raise AssertionError(
                "LexicalService must be immutable"
            )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    def test_display_name(self):

        service = LexicalService(
            repository=self._repository(),
        )

        assert service.display_name == "Lexical Service"

    def test_display_text(self):

        service = LexicalService(
            repository=self._repository(),
        )

        assert service.display_text == service.display_name

    def test_display_description(self):

        service = LexicalService(
            repository=self._repository(),
        )

        assert (
            service.display_description
            == "Domain façade for canonical lexical retrieval."
        )

    def test_string_representation(self):

        service = LexicalService(
            repository=self._repository(),
        )

        assert str(service) == service.display_text

    # ---------------------------------------------------------
    # Lookup Engine
    # ---------------------------------------------------------

    def test_lookup_engine_is_canonical_engine(self):

        repository = self._repository()

        service = LexicalService(
            repository=repository,
        )

        engine = service.lookup_engine

        assert isinstance(
            engine,
            LexicalLookupEngine,
        )

    def test_lookup_engine_uses_same_repository(self):

        repository = self._repository()

        service = LexicalService(
            repository=repository,
        )

        assert (
            service.lookup_engine.repository
            is repository
        )

    # ---------------------------------------------------------
    # Direct Repository Delegation
    # ---------------------------------------------------------

    def test_get_entry_delegates_to_repository(self):

        repository = self._repository()

        expected = object()

        repository.get_entry.return_value = expected

        service = LexicalService(
            repository=repository,
        )

        result = service.get_entry("राम")

        assert result is expected

        repository.get_entry.assert_called_once_with(
            "राम"
        )

    def test_lookup_lemma_delegates_to_repository(self):

        repository = self._repository()

        expected = ("entry-1", "entry-2")

        repository.find_entries_by_lemma.return_value = expected

        service = LexicalService(
            repository=repository,
        )

        result = service.lookup_lemma("राम")

        assert result is expected

        repository.find_entries_by_lemma.assert_called_once_with(
            "राम"
        )

    def test_lookup_word_form_delegates_to_repository(self):

        repository = self._repository()

        expected = ("entry-1",)

        repository.find_entries_by_word_form.return_value = expected

        service = LexicalService(
            repository=repository,
        )

        result = service.lookup_word_form("रामः")

        assert result is expected

        repository.find_entries_by_word_form.assert_called_once_with(
            "रामः"
        )

    def test_lookup_senses_delegates_to_repository(self):

        repository = self._repository()

        expected = ("sense-1", "sense-2")

        repository.find_senses.return_value = expected

        service = LexicalService(
            repository=repository,
        )

        result = service.lookup_senses("राम")

        assert result is expected

        repository.find_senses.assert_called_once_with(
            "राम"
        )

    def test_search_delegates_to_repository(self):

        repository = self._repository()

        expected = ("entry-1", "entry-2")

        repository.search.return_value = expected

        service = LexicalService(
            repository=repository,
        )

        result = service.search("rāma")

        assert result is expected

        repository.search.assert_called_once_with(
            "rāma"
        )

    def test_all_entries_delegates_to_repository(self):

        repository = self._repository()

        expected = ("entry-1", "entry-2")

        repository.all_entries.return_value = expected

        service = LexicalService(
            repository=repository,
        )

        result = service.all_entries()

        assert result is expected

        repository.all_entries.assert_called_once_with()

    def test_count_delegates_to_repository(self):

        repository = self._repository()

        repository.count = 42

        service = LexicalService(
            repository=repository,
        )

        assert service.count == 42

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def test_resolve_returns_lexical_resolution_result(self):

        repository = self._repository()

        repository.find_entries_by_word_form.return_value = ()

        service = LexicalService(
            repository=repository,
        )

        result = service.resolve(
            self._context()
        )

        assert result.context == self._context()
        assert result.succeeded is False
        assert result.candidate_count == 0

    def test_resolve_uses_context_subject_as_word_form(self):

        repository = self._repository()

        repository.find_entries_by_word_form.return_value = ()

        service = LexicalService(
            repository=repository,
        )

        service.resolve(
            self._context()
        )

        repository.find_entries_by_word_form.assert_called_once_with(
            "रामः"
        )

    # ---------------------------------------------------------
    # Resolution Contribution
    # ---------------------------------------------------------

    def test_contribute_enriches_resolution_result(self):

        repository = self._repository()

        repository.find_entries_by_word_form.return_value = ()

        service = LexicalService(
            repository=repository,
        )

        context = self._context()

        aggregate = ResolutionResult(
            context=context,
        )

        result = service.contribute(
            aggregate=aggregate,
            context=context,
        )

        assert result is not aggregate
        assert result.context is context
        assert result.lexical is not None
        assert result.has_lexical is True

    def test_contribute_preserves_context(self):

        repository = self._repository()

        repository.find_entries_by_word_form.return_value = ()

        service = LexicalService(
            repository=repository,
        )

        context = self._context()

        aggregate = ResolutionResult(
            context=context,
        )

        result = service.contribute(
            aggregate=aggregate,
            context=context,
        )

        assert result.context == aggregate.context
