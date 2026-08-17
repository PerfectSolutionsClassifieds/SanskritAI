
from __future__ import annotations

from SanskritAI.domain.sandhi.sandhi_service import (
    SandhiService,
)


class StubSandhiRepository:
    pass


def test_sandhi_service_can_be_constructed():

    repository = StubSandhiRepository()

    service = SandhiService(
        repository=repository,
    )

    assert service.repository is repository


def test_sandhi_service_exposes_resolution_kernel():

    repository = StubSandhiRepository()

    service = SandhiService(
        repository=repository,
    )

    kernel = service.resolution_kernel

    assert kernel is not None
    assert kernel.repository is repository
