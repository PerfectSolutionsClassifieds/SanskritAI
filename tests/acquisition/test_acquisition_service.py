from __future__ import annotations

import pytest

from SanskritAI.acquisition.services.acquisition_service import (
    AcquisitionService,
)


def test_acquisition_service_is_abstract():
    assert AcquisitionService.__abstractmethods__ == {"acquire"}


def test_acquisition_service_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AcquisitionService()
