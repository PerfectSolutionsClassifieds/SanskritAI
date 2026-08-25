
import pytest

from SanskritAI.domain.lexical.lexical_resolution_strategy import (
    LexicalResolutionStrategy,
)


def test_strategy_is_abstract():
    with pytest.raises(TypeError):
        LexicalResolutionStrategy()
