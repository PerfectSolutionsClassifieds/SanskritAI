
from dataclasses import replace
from pathlib import Path
import hashlib
import sys
import tempfile

REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from SanskritAI.acquisition.downloaders.local_file_importer import (
    LocalFileImporter,
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


# ------------------------------------------------------------------
# 1. Canonical artifact integrity
# ------------------------------------------------------------------

assert SOURCE.is_file(), (
    f"Missing canonical Amarakośa artifact: {SOURCE}"
)

source_size = SOURCE.stat().st_size
source_hash = sha256(SOURCE)

print("\nCanonical artifact:")
print("  path   :", SOURCE)
print("  size   :", source_size)
print("  sha256 :", source_hash)

assert source_size == 645456
assert source_hash == (
    "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190"
)

print("  integrity: PASS")


# ------------------------------------------------------------------
# 2. Production Amarakośa manifest contract
# ------------------------------------------------------------------

print("\n" + "-" * 72)
print("Production Amarakośa manifest")
print("-" * 72)

production_manifest = create_amarakosha_manifest()

production_source = production_manifest.source

print("manifest_id       :", production_manifest.manifest_id)
print("source_id         :", production_source.source_id)
print("source_type       :", production_source.source_type)
print("source_format     :", production_source.source_format)
print("source.local_path :", production_source.local_path)
print("manifest urls     :", production_manifest.urls)
print("manifest mirrors  :", production_manifest.mirrors)
print("metadata          :", production_manifest.metadata)
print("destination       :", production_manifest.destination_directory)

# The production canonical source location is carried by
# CorpusSource.local_path, not manifest.metadata["source_path"].
assert production_source.local_path is not None

production_local_path = Path(
    production_source.local_path
).resolve()

assert production_local_path == SOURCE.resolve()

assert production_manifest.urls == []
assert production_manifest.mirrors == []

print("\nProduction CorpusSource.local_path: PASS")
print("Production manifest has no remote URLs: PASS")


# ------------------------------------------------------------------
# 3. Document the current LocalFileImporter contract
# ------------------------------------------------------------------

print("\n" + "-" * 72)
print("LocalFileImporter contract")
print("-" * 72)

local_importer = LocalFileImporter()

print(
    "LocalFileImporter.supports() requires "
    "manifest.metadata['source_path']."
)

print(
    "Production manifest currently stores the canonical "
    "local path in CorpusSource.local_path."
)

print(
    "\nThis regression audit therefore creates an isolated "
    "adapter manifest using the existing LocalFileImporter "
    "contract. This does NOT modify production."
)


# ------------------------------------------------------------------
# 4. Isolated importer manifest
# ------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmp:

    destination = Path(tmp) / "destination"

    isolated_metadata = dict(
        production_manifest.metadata
    )

    isolated_metadata["source_path"] = str(
        production_source.local_path
    )

    isolated_manifest = replace(
        production_manifest,
        destination_directory=destination,
        metadata=isolated_metadata,
    )

    print("\n" + "-" * 72)
    print("Isolated LocalFileImporter manifest")
    print("-" * 72)

    print(
        "metadata[source_path] :",
        isolated_manifest.get_metadata("source_path"),
    )

    assert (
        isolated_manifest.get_metadata("source_path")
        == str(production_source.local_path)
    )

    print("metadata source_path: PASS")


    # ------------------------------------------------------------------
    # 5. LocalFileImporter.supports()
    # ------------------------------------------------------------------

    supports = local_importer.supports(
        isolated_manifest
    )

    print(
        "LocalFileImporter.supports(manifest):",
        supports,
    )

    assert supports is True

    print("LocalFileImporter support contract: PASS")


    # ------------------------------------------------------------------
    # 6. LocalFileImporter.download()
    # ------------------------------------------------------------------

    print("\n" + "-" * 72)
    print("Isolated local acquisition")
    print("-" * 72)

    result = local_importer.download(
        isolated_manifest
    )

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

    copied_size = copied.stat().st_size
    copied_hash = sha256(copied)

    print("\nCopied artifact:")
    print("  path   :", copied)
    print("  size   :", copied_size)
    print("  sha256 :", copied_hash)

    assert copied_size == source_size
    assert copied_hash == source_hash

    assert result.bytes_downloaded == source_size

    print("\nLocalFileImporter isolated acquisition: PASS")


# ------------------------------------------------------------------
# 7. Final architectural finding
# ------------------------------------------------------------------

print("\n" + "=" * 72)
print("13R-8F-2 RESULT")
print("=" * 72)

print(
    "PASS — LocalFileImporter correctly acquires the "
    "Amarakośa local artifact under its current contract."
)

print(
    "\nIMPORTANT CONTRACT FINDING:"
)

print(
    "Production Amarakośa source location:"
)

print(
    "    CorpusSource.local_path"
)

print(
    "\nLocalFileImporter discovery contract:"
)

print(
    "    manifest.metadata['source_path']"
)

print(
    "\nThese are currently different representations of the "
    "same local-source concept."
)

print(
    "\nNo production files were modified by this audit."
)

print(
    "\nTherefore 13R-8F-3 must NOT blindly delegate the "
    "production manifest yet."
)

print(
    "The next production step should first decide where the "
    "generic local-dispatch normalization belongs:"
)

print(
    "    DefaultSourceAcquirer"
    "  OR  LocalFileImporter"
    "  OR  canonical AcquisitionManifest contract"
)

print("=" * 72)
