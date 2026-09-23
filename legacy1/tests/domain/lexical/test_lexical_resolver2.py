
from unittest.mock import Mock

from SanskritAI.domain.lexical.lexical_resolver import (
    LexicalResolver,
)


def test_resolver_stores_strategy():
    strategy = Mock()

    resolver = LexicalResolver(
        strategy=strategy,
    )

    assert resolver.strategy is strategy


def test_resolver_delegates_to_strategy():
    strategy = Mock()

    expected = object()

    strategy.resolve.return_value = expected

    resolver = LexicalResolver(
        strategy=strategy,
    )

    context = object()

    result = resolver.resolve(
        context,
    )

    assert result is expected

    strategy.resolve.assert_called_once_with(
        context,
    )


def test_display_contract():
    resolver = LexicalResolver(
        strategy=Mock(),
    )

    assert resolver.display_name == "Lexical Resolver"
    assert "lexical resolution strategies" in (
        resolver.display_description
    )
