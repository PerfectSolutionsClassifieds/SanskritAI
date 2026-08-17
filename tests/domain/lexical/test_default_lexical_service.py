from __future__ import annotations

from unittest.mock import Mock

from SanskritAI.domain.lexical.default_lexical_service import (
    DefaultLexicalService,
)

from SanskritAI.domain.lexical.lexical_service import (
    LexicalService,
)

from SanskritAI.domain.lexical.lexical_lookup_engine import (
    LexicalLookupEngine,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


class TestDefaultLexicalService:

    def test_is_lexical_service(self):

        service = DefaultLexicalService(
            repository=Mock(),
        )

        assert isinstance(
            service,
            LexicalService,
        )

    def test_preserves_repository(self):

        repository = Mock()

        service = DefaultLexicalService(
            repository=repository,
        )

        assert service.repository is repository

    def test_display_name(self):

        service = DefaultLexicalService(
            repository=Mock(),
        )

        assert (
            service.display_name
            == "Default Lexical Service"
        )

    def test_display_text(self):

        service = DefaultLexicalService(
            repository=Mock(),
        )

        assert (
            service.display_text
            == "Default Lexical Service"
        )

    def test_display_description(self):

        service = DefaultLexicalService(
            repository=Mock(),
        )

        assert (
            service.display_description
            == "Canonical lexical resolution service."
        )

    def test_inherits_lookup_engine_behavior(self):

        repository = Mock()

        service = DefaultLexicalService(
            repository=repository,
        )

        assert isinstance(
            service.lookup_engine,
            LexicalLookupEngine,
        )

        assert (
            service.lookup_engine.repository
            is repository
        )

    def test_can_resolve_using_inherited_service_logic(self):

        repository = Mock()

        repository.find_entries_by_word_form.return_value = ()

        service = DefaultLexicalService(
            repository=repository,
        )

        context = ResolutionContext(
            identifier="test",
            subject="रामः",
        )

        result = service.resolve(
            context,
        )

        assert result.context == context
        assert result.succeeded is False
        assert result.candidate_count == 0

    def test_string_representation(self):

        service = DefaultLexicalService(
            repository=Mock(),
        )

        assert (
            str(service)
            == "Default Lexical Service"
        )
