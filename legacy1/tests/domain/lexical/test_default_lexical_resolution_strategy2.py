
from unittest.mock import Mock

from SanskritAI.domain.lexical.default_lexical_resolution_strategy import (
    DefaultLexicalResolutionStrategy,
)


def test_strategy_stores_lookup_engine():
    engine = Mock()

    strategy = DefaultLexicalResolutionStrategy(
        lookup_engine=engine,
    )

    assert strategy.lookup_engine is engine


def test_strategy_delegates_resolution():
    engine = Mock()

    expected = object()

    engine.lookup.return_value = expected

    strategy = DefaultLexicalResolutionStrategy(
        lookup_engine=engine,
    )

    context = object()

    result = strategy.resolve(
        context,
    )

    assert result is expected

    engine.lookup.assert_called_once_with(
        context,
    )


def test_display_contract():
    strategy = DefaultLexicalResolutionStrategy(
        lookup_engine=Mock(),
    )

    assert (
        strategy.display_name
        == "Default Lexical Resolution Strategy"
    )

    assert "LexicalLookupEngine" in (
        strategy.display_description
    )
