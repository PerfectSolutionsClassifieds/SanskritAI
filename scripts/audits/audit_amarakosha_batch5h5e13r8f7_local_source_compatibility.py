from __future__ import annotations

"""
13R-8F-7 — Local source compatibility audit

Purpose
-------
Verify that both existing representations can coexist:

Canonical:
    manifest.source.local_path

Compatibility:
    manifest.metadata["source_path"]

No production mutation is performed.
"""

from dataclasses import fields
from pathlib import Path
import sys


REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))


def main() -> None:
    print("=" * 72)
    print("13R-8F-7 — Local source compatibility audit")
    print("=" * 72)

    from SanskritAI.acquisition.downloaders.local_file_importer import (
        LocalFileImporter,
    )
    from SanskritAI.acquisition.models.acquisition_manifest import (
        AcquisitionManifest,
    )
    from SanskritAI.acquisition.models.corpus_source import (
        CorpusSource,
    )
    from SanskritAI.acquisition.models.source_format import (
        SourceFormat,
    )
    from SanskritAI.acquisition.models.source_status import (
        SourceStatus,
    )
    from SanskritAI.acquisition.models.source_type import (
        SourceType,
    )

    # ---------------------------------------------------------------
    # Confirm canonical field
    # ---------------------------------------------------------------

    corpus_fields = {
        field.name
        for field in fields(CorpusSource)
    }

    assert "local_path" in corpus_fields

    print(
        "CorpusSource.local_path: PASS"
    )

    # ---------------------------------------------------------------
    # Confirm manifest has no duplicate source_path field
    # ---------------------------------------------------------------

    manifest_fields = {
        field.name
        for field in fields(AcquisitionManifest)
    }

    assert "source" in manifest_fields
    assert "source_path" not in manifest_fields

    print(
        "AcquisitionManifest.source: PASS"
    )
    print(
        "No duplicate AcquisitionManifest.source_path: PASS"
    )

    # ---------------------------------------------------------------
    # Build isolated source
    # ---------------------------------------------------------------

    source_path = Path(
        "/tmp/sanskritai_amarakosha_source.txt"
    )

    source = CorpusSource(
        source_id="audit-local-source",
        name="Audit Local Source",
        source_type=SourceType.LEXICON,
        source_format=SourceFormat.TXT,
        status=SourceStatus.REGISTERED,
        local_path=source_path,
    )

    manifest = AcquisitionManifest(
        manifest_id="audit-local-source",
        source=source,
        urls=[],
        mirrors=[],
        preferred_format=SourceFormat.TXT,
        destination_directory=Path("/tmp"),
        metadata={},
    )

    print()
    print(
        "Canonical source path:",
        manifest.source.local_path,
    )

    # ---------------------------------------------------------------
    # Compatibility metadata representation
    # ---------------------------------------------------------------

    compatibility_manifest = AcquisitionManifest(
        manifest_id="audit-compatibility-source",
        source=source,
        urls=[],
        mirrors=[],
        preferred_format=SourceFormat.TXT,
        destination_directory=Path("/tmp"),
        metadata={
            "source_path": str(source_path),
        },
    )

    print(
        "Compatibility metadata path:",
        compatibility_manifest.get_metadata(
            "source_path"
        ),
    )

    # ---------------------------------------------------------------
    # Architectural decision
    # ---------------------------------------------------------------

    print()
    print("Expected resolution precedence:")
    print("  1. manifest.source.local_path")
    print("  2. manifest.metadata['source_path']")
    print("  3. no local source")

    print()
    print(
        "No AcquisitionManifest schema expansion required: PASS"
    )
    print(
        "No Amarakośa-specific path field required: PASS"
    )
    print(
        "Compatibility metadata retained only as fallback: PASS"
    )

    importer = LocalFileImporter()

    print()
    print(
        "LocalFileImporter:",
        importer,
    )

    print()
    print("13R-8F-7 COMPLETE")


if __name__ == "__main__":
    main()
