
from __future__ import annotations


def test_resolution_services_are_importable():

    from SanskritAI.domain.dhatu.dhatu_service import (
        DhatuService,
    )

    from SanskritAI.domain.morphology.morphological_service import (
        MorphologicalService,
    )

    from SanskritAI.domain.sandhi.sandhi_service import (
        SandhiService,
    )

    assert DhatuService is not None
    assert MorphologicalService is not None
    assert SandhiService is not None
