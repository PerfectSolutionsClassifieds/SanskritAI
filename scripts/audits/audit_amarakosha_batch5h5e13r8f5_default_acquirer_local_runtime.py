
from pathlib import Path
from dataclasses import replace
import hashlib
import tempfile
import sys


REPO_ROOT = Path(
    "/content/SanskritAI"
).resolve()

WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(WORKSPACE_ROOT),
    )


SOURCE_PATH = (
    REPO_ROOT / "amarakosha.txt"
).resolve()

EXPECTED_SIZE = 645456

EXPECTED_SHA256 = (
    "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190"
)


print("=" * 72)
print(
    "13R-8F-5 — DefaultSourceAcquirer local runtime"
)
print("=" * 72)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as source:

        for chunk in iter(
            lambda: source.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------

from SanskritAI.acquisition.acquirers.default_source_acquirer import (
    DefaultSourceAcquirer,
)

from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)

from SanskritAI.acquisition.models.source_status import (
    SourceStatus,
)

from SanskritAI.acquisition.sources.amarakosha import (
    create_amarakosha_source,
)

from SanskritAI.acquisition.sources.amarakosha_manifest import (
    create_amarakosha_manifest,
)


# ----------------------------------------------------------------------
# Canonical artifact integrity
# ----------------------------------------------------------------------

print("\n" + "-" * 72)
print("Canonical Amarakośa artifact")
print("-" * 72)

assert SOURCE_PATH.is_file(), (
    f"Canonical artifact missing: {SOURCE_PATH}"
)

actual_size = SOURCE_PATH.stat().st_size
actual_sha256 = sha256(SOURCE_PATH)

print(
    "path   :",
    SOURCE_PATH,
)

print(
    "size   :",
    actual_size,
)

print(
    "sha256 :",
    actual_sha256,
)

assert actual_size == EXPECTED_SIZE, (
    f"Unexpected Amarakośa artifact size: "
    f"{actual_size} != {EXPECTED_SIZE}"
)

assert actual_sha256 == EXPECTED_SHA256, (
    "Unexpected Amarakośa artifact SHA-256: "
    f"{actual_sha256} != {EXPECTED_SHA256}"
)

print(
    "integrity: PASS"
)


# ----------------------------------------------------------------------
# Production source
# ----------------------------------------------------------------------

print("\n" + "-" * 72)
print("Production Amarakośa source")
print("-" * 72)

source = create_amarakosha_source()

print(
    "source_id       :",
    source.source_id,
)

print(
    "source_type     :",
    source.source_type,
)

print(
    "source_format   :",
    source.source_format,
)

print(
    "source.local_path:",
    source.local_path,
)


assert source.source_id == "amarakosha"

assert (
    source.local_path is not None
)

canonical_local_path = Path(
    source.local_path
).resolve()

assert (
    canonical_local_path == SOURCE_PATH
), (
    "Production CorpusSource.local_path does not "
    "resolve to the canonical Amarakośa artifact."
)

print(
    "CorpusSource.local_path: PASS"
)


# ----------------------------------------------------------------------
# Production manifest
# ----------------------------------------------------------------------

print("\n" + "-" * 72)
print("Production Amarakośa manifest")
print("-" * 72)

manifest = create_amarakosha_manifest()

print(
    "manifest_id      :",
    manifest.manifest_id,
)

print(
    "source_id        :",
    manifest.source.source_id,
)

print(
    "source_type      :",
    manifest.source.source_type,
)

print(
    "source_format    :",
    manifest.source.source_format,
)

print(
    "source.local_path:",
    manifest.source.local_path,
)

print(
    "manifest urls    :",
    manifest.urls,
)

print(
    "manifest mirrors :",
    manifest.mirrors,
)

print(
    "destination      :",
    manifest.destination_directory,
)


assert (
    manifest.source.local_path is not None
)

assert (
    Path(
        manifest.source.local_path
    ).resolve()
    == SOURCE_PATH
)

assert manifest.urls == []

assert manifest.mirrors == []

print(
    "Production manifest canonical local-source "
    "contract: PASS"
)


# ----------------------------------------------------------------------
# IMPORTANT CONTRACT NORMALIZATION
#
# Production canonical location:
#
#     manifest.source.local_path
#
# Existing LocalFileImporter discovery contract:
#
#     manifest.metadata["source_path"]
#
# Do NOT mutate the production manifest.
#
# Build an isolated manifest copy and normalize the canonical
# CorpusSource.local_path into the LocalFileImporter contract.
# ----------------------------------------------------------------------

print("\n" + "-" * 72)
print("Local dispatch normalization")
print("-" * 72)

canonical_source_path = Path(
    manifest.source.local_path
).resolve()

isolated_metadata = dict(
    manifest.metadata
)

isolated_metadata[
    "source_path"
] = str(
    canonical_source_path
)


isolated_manifest = replace(
    manifest,
    metadata=isolated_metadata,
)


print(
    "canonical source path :",
    canonical_source_path,
)

print(
    "normalized metadata path:",
    isolated_manifest.get_metadata(
        "source_path"
    ),
)


assert (
    isolated_manifest.get_metadata(
        "source_path"
    )
    == str(canonical_source_path)
)

print(
    "source-path normalization: PASS"
)


# ----------------------------------------------------------------------
# Verify LocalFileImporter dispatch contract
# ----------------------------------------------------------------------

from SanskritAI.acquisition.downloaders.local_file_importer import (
    LocalFileImporter,
)


local_importer = LocalFileImporter()

supports_local = (
    local_importer.supports(
        isolated_manifest
    )
)

print(
    "LocalFileImporter.supports():",
    supports_local,
)

assert supports_local is True

print(
    "LocalFileImporter support after "
    "normalization: PASS"
)


# ----------------------------------------------------------------------
# Verify DefaultSourceAcquirer
# ----------------------------------------------------------------------

print("\n" + "-" * 72)
print("DefaultSourceAcquirer runtime")
print("-" * 72)

acquirer = DefaultSourceAcquirer()

print(
    "acquirer:",
    acquirer,
)


# ----------------------------------------------------------------------
# Isolated destination
# ----------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmp:

    destination = (
        Path(tmp)
        / "destination"
    )

    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    runtime_metadata = dict(
        isolated_manifest.metadata
    )

    runtime_manifest = replace(
        isolated_manifest,
        destination_directory=destination,
        metadata=runtime_metadata,
    )

    print(
        "runtime destination:",
        destination,
    )

    # --------------------------------------------------------------
    # Execute actual production DefaultSourceAcquirer.acquire()
    # --------------------------------------------------------------

    result = acquirer.acquire(
        runtime_manifest
    )

    print("\n" + "-" * 72)
    print("AcquisitionResult")
    print("-" * 72)

    print(
        "success          :",
        result.success,
    )

    print(
        "message          :",
        result.message,
    )

    print(
        "downloaded_files :",
        result.downloaded_files,
    )

    print(
        "bytes_downloaded :",
        result.bytes_downloaded,
    )

    print(
        "checksum_verified:",
        result.checksum_verified,
    )

    print(
        "license_verified :",
        result.license_verified,
    )

    print(
        "normalized       :",
        result.normalized,
    )

    print(
        "imported         :",
        result.imported,
    )

    print(
        "warnings         :",
        result.warnings,
    )

    print(
        "errors           :",
        result.errors,
    )

    # --------------------------------------------------------------
    # Runtime assertions
    # --------------------------------------------------------------

    assert result.success is True, (
        "DefaultSourceAcquirer local acquisition failed: "
        f"{result.errors}"
    )

    assert not result.errors

    assert result.downloaded_files

    copied = (
        result.downloaded_files[0]
    )

    assert copied.is_file()

    copied_size = copied.stat().st_size

    copied_sha256 = sha256(
        copied
    )

    print("\nCopied artifact:")
    print(
        "  path   :",
        copied,
    )
    print(
        "  size   :",
        copied_size,
    )
    print(
        "  sha256 :",
        copied_sha256,
    )

    assert (
        copied_size
        == EXPECTED_SIZE
    )

    assert (
        copied_sha256
        == EXPECTED_SHA256
    )

    assert (
        result.bytes_downloaded
        == EXPECTED_SIZE
    )

    print(
        "DefaultSourceAcquirer local runtime: PASS"
    )


# ----------------------------------------------------------------------
# Verify production manifest was not mutated by audit
# ----------------------------------------------------------------------

print("\n" + "-" * 72)
print("Production manifest immutability check")
print("-" * 72)

fresh_manifest = create_amarakosha_manifest()

assert (
    fresh_manifest.get_metadata(
        "source_path"
    )
    is None
), (
    "Production Amarakośa manifest unexpectedly acquired "
    "metadata['source_path']. The audit must not mutate "
    "the canonical manifest contract."
)

assert (
    fresh_manifest.source.local_path
    is not None
)

assert (
    Path(
        fresh_manifest.source.local_path
    ).resolve()
    == SOURCE_PATH
)

print(
    "Canonical manifest remains source.local_path-based: PASS"
)


# ----------------------------------------------------------------------
# Final result
# ----------------------------------------------------------------------

print("\n" + "=" * 72)
print("13R-8F-5 RESULT")
print("=" * 72)

print(
    "PASS — DefaultSourceAcquirer successfully "
    "acquired the Amarakośa local artifact through "
    "the generic LocalFileImporter dispatch boundary."
)

print(
    "\nVerified flow:"
)

print(
    "  CorpusSource.local_path"
    " -> isolated manifest normalization"
    " -> manifest.metadata['source_path']"
    " -> LocalFileImporter"
    " -> AcquisitionResult"
)

print(
    "\nProduction canonical manifest was not modified."
)

print(
    "\nThe audit does not change the production "
    "AcquisitionManifest contract."
)

print("=" * 72)
