
from dataclasses import replace
from pathlib import Path
import hashlib
import sys
import tempfile

REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from SanskritAI.acquisition.models.acquisition_manifest import AcquisitionManifest
from SanskritAI.acquisition.acquirers.default_source_acquirer import (
    DefaultSourceAcquirer,
)
from SanskritAI.acquisition.downloaders.local_file_importer import (
    LocalFileImporter,
)
from SanskritAI.acquisition.sources.amarakosha import (
    create_amarakosha_source,
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
print("13R-8F-2 — Generic local-dispatch regression contract")
print("=" * 72)

assert SOURCE.is_file(), f"Missing canonical artifact: {SOURCE}"

print("\nCanonical artifact:")
print("  path :", SOURCE)
print("  size :", SOURCE.stat().st_size)
print("  sha256:", sha256(SOURCE))

print("\n" + "-" * 72)
print("Production Amarakośa manifest")
print("-" * 72)

production_manifest = create_amarakosha_manifest()

print("manifest_id :", production_manifest.manifest_id)
print("source_id   :", production_manifest.source.source_id)
print("urls        :", production_manifest.urls)
print("mirrors     :", production_manifest.mirrors)
print(
    "source_path :",
    production_manifest.get_metadata("source_path"),
)
print(
    "destination :",
    production_manifest.destination_directory,
)

assert production_manifest.get_metadata("source_path") is not None
assert production_manifest.source.source_id == "amarakosha"

print("\n" + "-" * 72)
print("LocalFileImporter support contract")
print("-" * 72)

local_importer = LocalFileImporter()

assert local_importer.supports(production_manifest) is True

print("LocalFileImporter.supports(manifest): PASS")

print("\n" + "-" * 72)
print("Isolated local acquisition")
print("-" * 72)

with tempfile.TemporaryDirectory() as tmp:
    destination = Path(tmp) / "destination"

    test_manifest = replace(
        production_manifest,
        destination_directory=destination,
        metadata=dict(production_manifest.metadata),
    )

    result = local_importer.download(test_manifest)

    print("success          :", result.success)
    print("message          :", result.message)
    print("downloaded_files :", result.downloaded_files)
    print("bytes_downloaded :", result.bytes_downloaded)
    print("warnings         :", result.warnings)
    print("errors           :", result.errors)

    assert result.success is True
    assert not result.errors
    assert len(result.downloaded_files) == 1

    copied = result.downloaded_files[0]

    assert copied.is_file()
    assert copied.stat().st_size == SOURCE.stat().st_size
    assert sha256(copied) == sha256(SOURCE)

    print("\nLocalFileImporter isolated acquisition: PASS")

print("\n" + "-" * 72)
print("DefaultSourceAcquirer dispatch expectation")
print("-" * 72)

acquirer = DefaultSourceAcquirer()

print(
    """
Expected production behavior:

    if LocalFileImporter().supports(manifest):
        return LocalFileImporter().download(manifest)

This delegation must occur before _validate_manifest(),
because _validate_manifest() currently requires all_urls.
"""
)

print("Current production acquire() remains unmodified by this audit.")

print("\n" + "=" * 72)
print("13R-8F-2 RESULT: CONTRACT VERIFIED")
print("=" * 72)
print(
    "The existing LocalFileImporter is sufficient for generic "
    "local acquisition."
)
print(
    "The next production change should be a minimal delegation "
    "inside DefaultSourceAcquirer."
)
print("=" * 72)
