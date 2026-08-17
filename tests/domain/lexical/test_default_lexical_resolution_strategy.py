from __future__ import annotations

from unittest.mock import Mock

from SanskritAI.domain.lexical.default_lexical_resolution_strategy import (
    DefaultLexicalResolutionStrategy,
)

from SanskritAI.domain.lexical.lexical_lookup_engine import (
    LexicalLookupEngine,
)

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


class TestDefaultLexicalResolutionStrategy:

    def test_can_be_created(self):

        engine = Mock(
            spec=LexicalLookupEngine
        )

        strategy = DefaultLexicalResolutionStrategy(
            lookup_engine=engine,
        )

        assert strategy is not None

    def test_preserves_lookup_engine(self):

        engine = Mock(
            spec=LexicalLookupEngine
        )

        strategy = DefaultLexicalResolutionStrategy(
            lookup_engine=engine,
        )

        assert strategy.lookup_engine is engine

    def test_resolve_delegates_to_lookup_engine(self):

        engine = Mock(
            spec=LexicalLookupEngine
        )

        expected = Mock(
            spec=LexicalResolutionResult
        )

        engine.lookup.return_value = expected

        strategy = DefaultLexicalResolutionStrategy(
            lookup_engine=engine,
        )

        context = ResolutionContext(
            identifier="test",
            subject="रामः",
        )

        result = strategy.resolve(
            context,
        )

        assert result is expected

        engine.lookup.assert_called_once_with(
            context
        )

    def test_display_name(self):

        strategy = DefaultLexicalResolutionStrategy(
            lookup_engine=Mock(
                spec=LexicalLookupEngine
            ),
        )

        assert (
            strategy.display_name
            == "Default Lexical Resolution Strategy"
        )

    def test_display_description(self):

        strategy = DefaultLexicalResolutionStrategy(
            lookup_engine=Mock(
                spec=LexicalLookupEngine
            ),
        )

        assert (
            strategy.display_description
            == (
                "Delegates lexical resolution to the "
                "LexicalLookupEngine."
            )
        )

    def test_is_lexical_resolution_strategy(self):

        from SanskritAI.domain.lexical.lexical_resolution_strategy import (
            LexicalResolutionStrategy,
        )

        strategy = DefaultLexicalResolutionStrategy(
            lookup_engine=Mock(
                spec=LexicalLookupEngine
            ),
        )

        assert isinstance(
            strategy,
            LexicalResolutionStrategy,
        )
