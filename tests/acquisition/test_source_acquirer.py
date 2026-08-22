from __future__ import annotations

import pytest

from SanskritAI.acquisition.acquirers.source_acquirer import (
    SourceAcquirer,
)


def test_source_acquirer_is_abstract():
    assert SourceAcquirer.__abstractmethods__ == {"acquire"}


def test_source_acquirer_cannot_be_instantiated():
    with pytest.raises(TypeError):
        SourceAcquirer()
