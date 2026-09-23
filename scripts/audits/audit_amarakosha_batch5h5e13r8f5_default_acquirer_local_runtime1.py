
from dataclasses import replace
from pathlib import Path
import hashlib
import sys
import tempfile

REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from SanskritAI.acquisition.acquirers.default_source_acquirer import (
    DefaultSourceAcquirer,
)
from SanskritAI.acquisition.sources.amarakosha_manifest import (
    create_amarakosha_manifest,
)


SOURCE = REPO_ROOT / "amarakosha.txt"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


print("=" * 72)
print("13R-8F-5 — DefaultSourceAcquirer local runtime")
print("=" * 72)

manifest = create_amarakosha_manifest()

assert manifest.get_metadata("source_path") is not None
assert manifest.urls == []
assert manifest.mirrors == []

print("\nInput manifest:")
print("  manifest_id :", manifest.manifest_id)
print("  source_id   :", manifest.source.source_id)
print("  source_path :", manifest.get_metadata("source_path"))
print("  urls        :", manifest.urls)
print("  mirrors     :", manifest.mirrors)

with tempfile.TemporaryDirectory() as tmp:
    destination = Path(tmp) / "destination"

    runtime_manifest = replace(
        manifest,
        destination_directory=destination,
        metadata=dict(manifest.metadata),
    )

    print("\nRunning:")
    print("  DefaultSourceAcquirer.acquire(manifest)")

    result = DefaultSourceAcquirer().acquire(
        runtime_manifest
    )

    print("\nResult:")
    print("  success          :", result.success)
    print("  message          :", result.message)
    print("  downloaded_files :", result.downloaded_files)
    print("  bytes_downloaded :", result.bytes_downloaded)
    print("  checksum_verified:", result.checksum_verified)
    print("  license_verified :", result.license_verified)
    print("  normalized       :", result.normalized)
    print("  imported         :", result.imported)
    print("  warnings         :", result.warnings)
    print("  errors           :", result.errors)

    assert result.success is True
    assert not result.errors
    assert len(result.downloaded_files) == 1

    copied = result.downloaded_files[0]

    assert copied.is_file()
    assert copied.stat().st_size == SOURCE.stat().st_size
    assert sha256(copied) == sha256(SOURCE)

    print("\nCopied file:")
    print("  path :", copied)
    print("  size :", copied.stat().st_size)
    print("  sha256:", sha256(copied))

print("\n" + "=" * 72)
print("13R-8F-5 RESULT: PASS")
print("=" * 72)
print(
    "DefaultSourceAcquirer successfully delegated the local "
    "manifest to LocalFileImporter."
)
print("=" * 72)
