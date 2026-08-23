
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Acquisition Manifest

Defines the acquisition policy for the Monier-Williams source.

This module deliberately does not perform downloading.
"""

from pathlib import Path

from SanskritAI.acquisition.sources.monier_williams import (
    MonierWilliamsSource,
)
from SanskritAI.domain.acquisition.acquisition_manifest import (
    AcquisitionManifest,
)


MW_SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "sanskrit-lexicon/csl-orig/"
    "master/v02/mw/mw.txt"
)


def create_monier_williams_manifest(
    *,
    destination: Path,
) -> AcquisitionManifest:
    """
    Create the canonical acquisition manifest for MW.

    Parameters
    ----------
    destination:
        Directory into which the acquired MW source is written.
    """

    source = MonierWilliamsSource()

    return AcquisitionManifest(
        source=source,
        destination=destination,
        urls=[
            MW_SOURCE_URL,
        ],
        expected_filename="mw.txt",
        overwrite_existing=False,
    )
