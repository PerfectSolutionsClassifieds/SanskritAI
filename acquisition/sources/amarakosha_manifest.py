
from __future__ import annotations

from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)
from SanskritAI.acquisition.models.source_format import SourceFormat

from SanskritAI.acquisition.sources.amarakosha import (
    AMARAKOSHA_ARTIFACT,
    AMARAKOSHA_PROVENANCE_URL,
    AMARAKOSHA_SHA256,
    create_amarakosha_source,
)


AMARAKOSHA_MANIFEST_ID = "amarakosha-local-txt"


def create_amarakosha_manifest() -> AcquisitionManifest:
    """
    Create the production acquisition manifest for the verified
    local Amarakośa TXT artifact.
    """

    if not AMARAKOSHA_ARTIFACT.exists():
        raise FileNotFoundError(
            f"Amarakośa artifact not found: "
            f"{AMARAKOSHA_ARTIFACT}"
        )

    if not AMARAKOSHA_ARTIFACT.is_file():
        raise ValueError(
            f"Amarakośa artifact is not a file: "
            f"{AMARAKOSHA_ARTIFACT}"
        )

    source = create_amarakosha_source()

    return AcquisitionManifest(
        manifest_id=AMARAKOSHA_MANIFEST_ID,
        source=source,
        urls=[],
        mirrors=[],
        preferred_format=SourceFormat.TXT,
        expected_filename=AMARAKOSHA_ARTIFACT.name,
        expected_size=AMARAKOSHA_ARTIFACT.stat().st_size,
        checksum=AMARAKOSHA_SHA256,
        checksum_algorithm="sha256",
        destination_directory=AMARAKOSHA_ARTIFACT.parent,
        cache_directory=None,
        overwrite_existing=False,
        extract_archives=False,
        importer="amarakosha",
        encoding="utf-8",
        normalize_unicode=True,
        validate_checksum=True,
        validate_license=True,
        priority=100,
        enabled=True,
        metadata={
            "filename": AMARAKOSHA_ARTIFACT.name,
            "encoding": "utf-8",
            "size_bytes": AMARAKOSHA_ARTIFACT.stat().st_size,
            "sha256": AMARAKOSHA_SHA256,
            "provenance_url": AMARAKOSHA_PROVENANCE_URL,
            "artifact_provenance": (
                "Embedded metadata in verified "
                "amarakosha.txt artifact."
            ),
            "acquisition_mode": "local",
            "provenance_relationship": (
                "Sanskrit Documents PDFs are verified "
                "external representations; direct PDF-to-TXT "
                "derivation is not established."
            ),
        },
    )


def get_amarakosha_manifest() -> AcquisitionManifest:
    return create_amarakosha_manifest()
    
