from __future__ import annotations

from unittest.mock import Mock

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.lexical.lexical_resolution_strategy import (
    LexicalResolutionStrategy,
)

from SanskritAI.domain.lexical.lexical_resolver import (
    LexicalResolver,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


class TestLexicalResolver:

    def test_can_be_created(self):

        strategy = Mock(
            spec=LexicalResolutionStrategy
        )

        resolver = LexicalResolver(
            strategy= strategy,
        )

        assert resolver is not None

    def test_preserves_strategy(self):

        strategy = Mock(
            spec=LexicalResolutionStrategy
        )

        resolver = LexicalResolver(
            strategy=strategy,
        )

        assert resolver.strategy is strategy

    def test_resolve_delegates_to_strategy(self):

        strategy = Mock(
            spec=LexicalResolutionStrategy
        )

        expected = Mock(
            spec=LexicalResolutionResult
        )

        strategy.resolve.return_value = expected

        resolver = LexicalResolver(
            strategy=strategy,
        )

        context = ResolutionContext(
            identifier="test",
            subject="रामः",
        )

        result = resolver.resolve(
            context,
        )

        assert result is expected

        strategy.resolve.assert_called_once_with(
            context
        )

    def test_display_name(self):

        resolver = LexicalResolver(
            strategy=Mock(
                spec=LexicalResolutionStrategy
            ),
        )

        assert (
            resolver.display_name
            == "Lexical Resolver"
        )

    def test_display_description(self):

        resolver = LexicalResolver(
            strategy=Mock(
                spec=LexicalResolutionStrategy
            ),
        )

        assert (
            resolver.display_description
            == "Facade over lexical resolution strategies."
        )

    def test_string_representation(self):

        resolver = LexicalResolver(
            strategy=Mock(
                spec=LexicalResolutionStrategy
            ),
        )

        assert (
            str(resolver)
            == resolver.display_text
        )
