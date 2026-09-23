
from __future__ import annotations

from pathlib import Path
import hashlib
import shutil
import sys
import tempfile


REPO_ROOT = Path("/content/SanskritAI").resolve()
REPO_PARENT = REPO_ROOT.parent.resolve()

if str(REPO_PARENT) not in sys.path:
    sys.path.insert(0, str(REPO_PARENT))


from SanskritAI.acquisition.downloaders.local_file_importer import (
    LocalFileImporter,
)
from SanskritAI.acquisition.sources.amarakosha_manifest import (
    create_amarakosha_manifest,
)


SOURCE = REPO_ROOT / "amarakosha.txt"

EXPECTED_SHA256 = (
    "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


print("=" * 72)
print("13R-8E-1 — Amarakośa LocalFileImporter runtime probe")
print("=" * 72)

print(f"Source : {SOURCE}")

if not SOURCE.exists() or not SOURCE.is_file():
    raise SystemExit("ABORT — canonical Amarakośa artifact missing.")

actual_hash = sha256(SOURCE)

if actual_hash != EXPECTED_SHA256:
    raise SystemExit(
        "ABORT — canonical Amarakośa artifact checksum mismatch."
    )

print("Source integrity : PASS")

manifest = create_amarakosha_manifest()

print()
print("-" * 72)
print("Manifest before local-importer adaptation")
print("-" * 72)

print(f"manifest_id        : {manifest.manifest_id}")
print(f"source_id          : {manifest.source.source_id}")
print(f"preferred_format   : {manifest.preferred_format}")
print(f"destination        : {manifest.destination_directory}")
print(f"expected_filename  : {manifest.expected_filename}")
print(f"expected_size      : {manifest.expected_size}")
print(f"checksum           : {manifest.checksum}")
print(f"urls               : {manifest.urls}")
print(f"mirrors            : {manifest.mirrors}")

# IMPORTANT:
# Never execute against the canonical artifact itself.
# Use a temporary destination outside the source path.
with tempfile.TemporaryDirectory(
    prefix="sanskritai_amarakosha_runtime_"
) as tmp:

    destination = Path(tmp)

    probe_manifest = manifest

    # AcquisitionManifest is a dataclass. Reconstruct it through replace()
    # rather than changing production code.
    from dataclasses import replace

    metadata = dict(manifest.metadata)
    metadata["source_path"] = str(SOURCE)

    probe_manifest = replace(
        manifest,
        destination_directory=destination,
        overwrite_existing=True,
        metadata=metadata,
    )

    print()
    print("-" * 72)
    print("Safe runtime destination")
    print("-" * 72)

    print(f"temporary destination : {destination}")

    importer = LocalFileImporter()

    supported = importer.supports(probe_manifest)

    print(f"LocalFileImporter.supports : {supported}")

    if not supported:
        raise SystemExit(
            "RESULT: BLOCKED — LocalFileImporter does not select "
            "a manifest carrying source_path."
        )

    print("Importer selection : PASS")

    result = importer.download(probe_manifest)

    print()
    print("-" * 72)
    print("AcquisitionResult")
    print("-" * 72)

    print(f"success          : {result.success}")
    print(f"status           : {result.status}")
    print(f"local_path       : {result.local_path}")
    print(f"bytes_downloaded : {result.bytes_downloaded}")
    print(f"errors           : {result.errors}")
    print(f"warnings         : {result.warnings}")

    acquired = destination / SOURCE.name

    if not acquired.exists():
        raise SystemExit(
            "RESULT: FAIL — LocalFileImporter did not create the "
            "expected temporary artifact."
        )

    print()
    print(f"temporary artifact exists : {acquired.exists()}")
    print(f"temporary artifact size   : {acquired.stat().st_size}")

    acquired_hash = sha256(acquired)

    print(f"temporary artifact SHA256 : {acquired_hash}")

    if acquired_hash != EXPECTED_SHA256:
        raise SystemExit(
            "RESULT: FAIL — temporary acquisition checksum mismatch."
        )

    print("temporary artifact integrity : PASS")

    if not result.success:
        raise SystemExit(
            "RESULT: FAIL — LocalFileImporter runtime acquisition "
            "returned unsuccessful result."
        )

print()
print("=" * 72)
print("RESULT: PASS — LocalFileImporter can safely acquire Amarakośa")
print("from the canonical local artifact into an isolated destination.")
print("=" * 72)
