from __future__ import annotations

"""
SanskritAI
==========

Amarakośa Corpus Source Definition
-----------------------------------

Defines the canonical Amarakośa source used by SanskritAI.

This module describes the currently verified local Amarakośa artifact:

    /content/SanskritAI/amarakosha.txt

It does NOT:

    - download the source
    - parse Amarakośa records
    - normalize lexical entries
    - build synsets
    - persist canonical lexical data
    - perform lexical lookup

Those responsibilities remain in their existing acquisition,
Amarakośa parser/importer, and canonical lexical layers.
"""

from pathlib import Path

from SanskritAI.acquisition.factories.corpus_source_factory import (
    CorpusSourceFactory,
)
from SanskritAI.acquisition.models.corpus_source import CorpusSource
from SanskritAI.acquisition.models.source_format import SourceFormat
from SanskritAI.acquisition.models.source_status import SourceStatus
from SanskritAI.acquisition.models.source_type import SourceType


AMARAKOSHA_SOURCE_ID = "amarakosha"

AMARAKOSHA_NAME = "Amarakośa"

AMARAKOSHA_ARTIFACT = (
    Path("/content/SanskritAI/amarakosha.txt")
)

AMARAKOSHA_SHA256 = (
    "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190"
)

AMARAKOSHA_PROVENANCE_URL = (
    "http://sanskrit.uohyd.ac.in/scl/"
)


def create_amarakosha_source() -> CorpusSource:
    """
    Create the canonical Amarakośa CorpusSource.

    The source is currently represented by the verified local
    UTF-8 text artifact already present in the repository checkout.

    No remote acquisition URL is asserted here because the exact
    downloadable source endpoint has not yet been established.
    """

    if not AMARAKOSHA_ARTIFACT.exists():
        raise FileNotFoundError(
            f"Verified Amarakośa artifact not found: "
            f"{AMARAKOSHA_ARTIFACT}"
        )

    if not AMARAKOSHA_ARTIFACT.is_file():
        raise ValueError(
            f"Amarakośa artifact is not a file: "
            f"{AMARAKOSHA_ARTIFACT}"
        )

    metadata = {
        "filename": AMARAKOSHA_ARTIFACT.name,
        "encoding": "utf-8",
        "size_bytes": AMARAKOSHA_ARTIFACT.stat().st_size,
        "sha256": AMARAKOSHA_SHA256,
        "provenance_url": AMARAKOSHA_PROVENANCE_URL,
        "artifact_provenance": (
            "Embedded metadata in verified amarakosha.txt artifact."
        ),
    }

    return CorpusSourceFactory.from_metadata(
        identifier=AMARAKOSHA_SOURCE_ID,
        title=AMARAKOSHA_NAME,
        source_type=SourceType.LEXICON,
        source_format=SourceFormat.TXT,
        status=SourceStatus.REGISTERED,
        local_path=AMARAKOSHA_ARTIFACT,
        download_url=None,
        checksum=AMARAKOSHA_SHA256,
        description=(
            "Canonical Amarakośa lexical source represented by "
            "the verified local UTF-8 text artifact."
        ),
        license=None,
        metadata=metadata,
    )


def get_amarakosha_source() -> CorpusSource:
    """
    Return the canonical Amarakośa CorpusSource.
    """
    return create_amarakosha_source()


__all__ = [
    "AMARAKOSHA_ARTIFACT",
    "AMARAKOSHA_NAME",
    "AMARAKOSHA_PROVENANCE_URL",
    "AMARAKOSHA_SHA256",
    "AMARAKOSHA_SOURCE_ID",
    "create_amarakosha_source",
    "get_amarakosha_source",
]
