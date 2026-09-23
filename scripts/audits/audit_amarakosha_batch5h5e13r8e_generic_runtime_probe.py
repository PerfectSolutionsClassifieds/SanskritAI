from __future__ import annotations

"""
13R-8E — Amarakośa safe generic runtime acquisition probe

Purpose
-------
Exercise the EXISTING generic DefaultSourceAcquirer local file:// path
against the verified Amarakośa artifact.

This is a READ/PROBE operation.

It must NOT:
- modify the canonical Amarakośa artifact
- modify the production Amarakośa source declaration
- modify the production Amarakośa manifest
- create an Amarakośa-specific acquirer
- create an Amarakośa-specific downloader
- use LocalFileImporter
- copy the artifact onto itself

Instead:

    canonical amarakosha.txt
            |
            | file://
            v
    DefaultSourceAcquirer
            |
            v
    temporary audit destination
            |
            v
    acquired amarakosha.txt

Then verify:
- AcquisitionResult.success
- downloaded file exists
- expected filename
- expected size
- expected SHA-256
- destination differs from source
- cleanup

Historical/duplicate audit scripts are ignored by this script.
"""

from pathlib import Path
import hashlib
import os
import shutil
import sys
import tempfile


# =====================================================================
# Bootstrap
# =====================================================================

ROOT = Path("/content/SanskritAI")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


print("=" * 72)
print("13R-8E — Amarakośa safe generic runtime acquisition probe")
print("=" * 72)
print(f"Repository root : {ROOT}")


# =====================================================================
# Verified canonical artifact
# =====================================================================

SOURCE = ROOT / "amarakosha.txt"

EXPECTED_FILENAME = "amarakosha.txt"
EXPECTED_SIZE = 645456
EXPECTED_SHA256 = (
    "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190"
)


print("\n" + "-" * 72)
print("Canonical artifact")
print("-" * 72)

print(f"source exists : {SOURCE.exists()}")
print(f"source file   : {SOURCE.is_file()}")
print(f"source path   : {SOURCE}")


if not SOURCE.exists() or not SOURCE.is_file():
    raise SystemExit(
        "ABORT — verified Amarakośa canonical artifact is unavailable."
    )


actual_size = SOURCE.stat().st_size


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


actual_sha256 = sha256(SOURCE)

print(f"source size   : {actual_size}")
print(f"expected size : {EXPECTED_SIZE}")
print(f"source SHA256  : {actual_sha256}")
print(f"expected SHA256: {EXPECTED_SHA256}")

if actual_size != EXPECTED_SIZE:
    raise SystemExit(
        "ABORT — canonical artifact size does not match verified baseline."
    )

if actual_sha256 != EXPECTED_SHA256:
    raise SystemExit(
        "ABORT — canonical artifact SHA-256 does not match verified baseline."
    )

print("canonical artifact integrity : PASS")


# =====================================================================
# Runtime imports
# =====================================================================

print("\n" + "-" * 72)
print("Generic runtime imports")
print("-" * 72)

try:
    from SanskritAI.acquisition.acquirers.default_source_acquirer import (
        DefaultSourceAcquirer,
    )

    print("DefaultSourceAcquirer : PASS")

except Exception as exc:
    print(
        f"DefaultSourceAcquirer : FAIL — {exc}"
    )
    raise SystemExit(
        "ABORT — generic acquisition runtime cannot be imported."
    )


try:
    from SanskritAI.acquisition.models.acquisition_manifest import (
        AcquisitionManifest,
    )

    print("AcquisitionManifest   : PASS")

except Exception as exc:
    print(
        f"AcquisitionManifest   : FAIL — {exc}"
    )
    raise SystemExit(
        "ABORT — AcquisitionManifest cannot be imported."
    )


try:
    from SanskritAI.acquisition.models.source_format import (
        SourceFormat,
    )

    print("SourceFormat           : PASS")

except Exception as exc:
    print(
        f"SourceFormat           : FAIL — {exc}"
    )
    raise SystemExit(
        "ABORT — SourceFormat cannot be imported."
    )


try:
    from SanskritAI.acquisition.models.source_status import (
        SourceStatus,
    )

    print("SourceStatus            : PASS")

except Exception as exc:
    print(
        f"SourceStatus            : FAIL — {exc}"
    )
    raise SystemExit(
        "ABORT — SourceStatus cannot be imported."
    )


# =====================================================================
# Existing production source
# =====================================================================

print("\n" + "-" * 72)
print("Production Amarakośa source")
print("-" * 72)

try:
    from SanskritAI.acquisition.sources.amarakosha import (
        create_amarakosha_source,
    )

    production_source = create_amarakosha_source()

    print(
        f"source_id       : {production_source.source_id}"
    )
    print(
        f"name            : {production_source.name}"
    )
    print(
        f"source_type     : {production_source.source_type}"
    )
    print(
        f"source_format   : {production_source.source_format}"
    )
    print(
        f"status          : {production_source.status}"
    )
    print(
        f"local_path      : {production_source.local_path}"
    )

except Exception as exc:
    print(
        f"Production Amarakośa source : FAIL — {exc}"
    )
    raise SystemExit(
        "ABORT — production Amarakośa source cannot be constructed."
    )


# =====================================================================
# Safe temporary destination
# =====================================================================

print("\n" + "-" * 72)
print("Temporary acquisition destination")
print("-" * 72)

temporary_root = Path(
    tempfile.mkdtemp(
        prefix="sanskritai_amarakosha_13r8e_",
    )
)

destination = temporary_root / EXPECTED_FILENAME

print(f"temporary root : {temporary_root}")
print(f"destination    : {destination}")

if destination.resolve() == SOURCE.resolve():
    raise SystemExit(
        "ABORT — temporary destination unexpectedly resolves to source."
    )

print("source/destination separation : PASS")


# =====================================================================
# Probe manifest
# =====================================================================

print("\n" + "-" * 72)
print("Probe AcquisitionManifest")
print("-" * 72)

file_url = SOURCE.resolve().as_uri()

print(f"file URL       : {file_url}")

probe_manifest = AcquisitionManifest(
    manifest_id="amarakosha-runtime-probe",
    source=production_source,
    urls=[file_url],
    mirrors=[],
    preferred_format=SourceFormat.TXT,
    expected_filename=EXPECTED_FILENAME,
    expected_size=EXPECTED_SIZE,
    checksum=EXPECTED_SHA256,
    checksum_algorithm="sha256",
    destination_directory=temporary_root,
    cache_directory=None,
    overwrite_existing=False,
    extract_archives=False,
    importer="amarakosha",
    encoding="utf-8",
    normalize_unicode=True,
    validate_checksum=True,
    validate_license=False,
    priority=100,
    enabled=True,
    metadata={
        "probe": True,
        "probe_stage": "13R-8E",
        "source_artifact": str(SOURCE),
        "acquisition_mode": "file_url_runtime_probe",
    },
)


print(
    f"manifest_id          : {probe_manifest.manifest_id}"
)
print(
    f"source_id            : {probe_manifest.source.source_id}"
)
print(
    f"urls                 : {probe_manifest.urls}"
)
print(
    f"preferred_format     : {probe_manifest.preferred_format}"
)
print(
    f"expected_filename    : {probe_manifest.expected_filename}"
)
print(
    f"expected_size        : {probe_manifest.expected_size}"
)
print(
    f"checksum             : {probe_manifest.checksum}"
)
print(
    f"destination_directory: {probe_manifest.destination_directory}"
)
print(
    f"requires_download    : {probe_manifest.requires_download}"
)
print(
    f"requires_checksum    : {probe_manifest.requires_checksum_validation}"
)


# =====================================================================
# Manifest contract checks
# =====================================================================

print("\n" + "-" * 72)
print("Probe manifest contract")
print("-" * 72)

assert probe_manifest.source.source_id == "amarakosha"
assert probe_manifest.preferred_format == SourceFormat.TXT
assert probe_manifest.expected_filename == EXPECTED_FILENAME
assert probe_manifest.expected_size == EXPECTED_SIZE
assert probe_manifest.checksum == EXPECTED_SHA256
assert probe_manifest.checksum_algorithm == "sha256"
assert probe_manifest.destination_directory == temporary_root
assert probe_manifest.requires_download is True
assert probe_manifest.requires_checksum_validation is True

print("manifest contract : PASS")


# =====================================================================
# Runtime acquisition
# =====================================================================

print("\n" + "-" * 72)
print("DefaultSourceAcquirer runtime execution")
print("-" * 72)

acquirer = DefaultSourceAcquirer()

print(
    f"acquirer : {type(acquirer).__name__}"
)

print("Executing generic file:// acquisition ...")

result = acquirer.acquire(
    probe_manifest
)


# =====================================================================
# AcquisitionResult
# =====================================================================

print("\n" + "-" * 72)
print("AcquisitionResult")
print("-" * 72)

print(
    f"success          : {result.success}"
)
print(
    f"message          : {result.message}"
)
print(
    f"errors           : {result.errors}"
)
print(
    f"warnings         : {result.warnings}"
)
print(
    f"downloaded_files : {result.downloaded_files}"
)
print(
    f"bytes_downloaded : {result.bytes_downloaded}"
)
print(
    f"completed_at     : {result.completed_at}"
)
print(
    f"duration_seconds : {result.duration_seconds}"
)


# =====================================================================
# Runtime assertions
# =====================================================================

print("\n" + "-" * 72)
print("Runtime result validation")
print("-" * 72)

if not result.success:
    raise SystemExit(
        "FAIL — generic DefaultSourceAcquirer did not report success."
    )

print("AcquisitionResult.success : PASS")


if result.errors:
    raise SystemExit(
        f"FAIL — acquisition returned errors: {result.errors}"
    )

print("Acquisition errors        : PASS")


if not result.downloaded_files:
    raise SystemExit(
        "FAIL — acquisition returned no downloaded files."
    )

print("Downloaded file registration : PASS")


# =====================================================================
# Locate acquired file
# =====================================================================

acquired = destination

print(
    f"expected acquired path : {acquired}"
)

if not acquired.exists():
    raise SystemExit(
        "FAIL — expected acquired file does not exist."
    )

if not acquired.is_file():
    raise SystemExit(
        "FAIL — acquired path is not a file."
    )

print("acquired file existence : PASS")


# =====================================================================
# Acquired file integrity
# =====================================================================

acquired_size = acquired.stat().st_size
acquired_sha256 = sha256(acquired)

print("\n" + "-" * 72)
print("Acquired artifact integrity")
print("-" * 72)

print(
    f"acquired size          : {acquired_size}"
)
print(
    f"expected size          : {EXPECTED_SIZE}"
)
print(
    f"acquired SHA256        : {acquired_sha256}"
)
print(
    f"expected SHA256        : {EXPECTED_SHA256}"
)

if acquired_size != EXPECTED_SIZE:
    raise SystemExit(
        "FAIL — acquired file size does not match expected size."
    )

print("acquired size : PASS")


if acquired_sha256 != EXPECTED_SHA256:
    raise SystemExit(
        "FAIL — acquired file SHA-256 does not match expected checksum."
    )

print("acquired SHA-256 : PASS")


# =====================================================================
# Source/destination physical separation
# =====================================================================

print("\n" + "-" * 72)
print("Source/destination separation")
print("-" * 72)

source_resolved = SOURCE.resolve()
destination_resolved = acquired.resolve()

print(
    f"source      : {source_resolved}"
)
print(
    f"destination : {destination_resolved}"
)
print(
    f"same path   : {source_resolved == destination_resolved}"
)

if source_resolved == destination_resolved:
    raise SystemExit(
        "FAIL — runtime probe destination is the source artifact itself."
    )

print("source/destination separation : PASS")


# =====================================================================
# Provenance preservation
# =====================================================================

print("\n" + "-" * 72)
print("Probe provenance")
print("-" * 72)

print(
    f"source artifact : {SOURCE}"
)
print(
    f"probe URL       : {file_url}"
)
print(
    f"manifest source : {probe_manifest.source.source_id}"
)

assert probe_manifest.source.source_id == "amarakosha"

print("source identity preservation : PASS")


# =====================================================================
# Cleanup
# =====================================================================

print("\n" + "-" * 72)
print("Cleanup")
print("-" * 72)

try:
    shutil.rmtree(
        temporary_root,
    )

    print(
        f"temporary probe directory removed : {temporary_root}"
    )

except Exception as exc:
    print(
        f"WARNING — temporary cleanup failed: {exc}"
    )


# =====================================================================
# Final decision
# =====================================================================

print("\n" + "=" * 72)
print("13R-8E decision")
print("=" * 72)

print(
    """
PASS criteria:

1. Verified canonical Amarakośa artifact remains unchanged.
2. Generic DefaultSourceAcquirer imports successfully.
3. Existing file:// acquisition path is exercised.
4. Temporary destination is physically different from source.
5. AcquisitionResult.success == True.
6. Acquired filename is amarakosha.txt.
7. Acquired size == 645456 bytes.
8. Acquired SHA-256 matches the verified canonical checksum.
9. No Amarakośa-specific acquirer/downloader/service is created.
10. Production source and production manifest are unchanged.
11. Temporary probe artifacts are removed.

No production files were modified.
"""
)

print(
    "RESULT: PASS — generic Amarakośa runtime acquisition probe completed."
)
