
from pathlib import Path
import hashlib
import shutil
import sys
import tempfile
from dataclasses import replace

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


EXPECTED_SHA256 = (
    "d82a5234e4bc15ef295b1b375a6548e02df9a10d6eb94e0f97223289c46c3190"
)

EXPECTED_SIZE = 645456

SOURCE = REPO_ROOT / "amarakosha.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


print("=" * 72)
print("13R-8E-1B — Amarakośa LocalFileImporter integrity probe")
print("=" * 72)

# ----------------------------------------------------------------------
# 1. Canonical source integrity
# ----------------------------------------------------------------------

assert SOURCE.is_file(), f"Missing source: {SOURCE}"
assert SOURCE.stat().st_size == EXPECTED_SIZE
assert sha256(SOURCE) == EXPECTED_SHA256

print("Canonical source integrity : PASS")


# ----------------------------------------------------------------------
# 2. Production manifest
# ----------------------------------------------------------------------

manifest = create_amarakosha_manifest()

print()
print("-" * 72)
print("Production manifest")
print("-" * 72)

print("manifest_id       :", manifest.manifest_id)
print("source_id         :", manifest.source.source_id)
print("preferred_format  :", manifest.preferred_format.value)
print("destination       :", manifest.destination_directory)
print("expected_filename :", manifest.expected_filename)
print("expected_size     :", manifest.expected_size)
print("checksum          :", manifest.checksum)
print("urls              :", manifest.urls)
print("mirrors           :", manifest.mirrors)


# ----------------------------------------------------------------------
# 3. Safe temporary destination
# ----------------------------------------------------------------------

probe_root = Path(
    tempfile.mkdtemp(
        prefix="sanskritai_amarakosha_import_"
    )
)

destination = probe_root / "destination"
destination.mkdir(parents=True, exist_ok=True)

print()
print("-" * 72)
print("Safe runtime destination")
print("-" * 72)

print("temporary root :", probe_root)
print("destination    :", destination)


# ----------------------------------------------------------------------
# 4. Build an isolated probe manifest
#
# IMPORTANT:
# Do not modify the production manifest.
#
# LocalFileImporter.supports() uses source_path metadata.
# LocalFileImporter.download() uses source_path and
# destination_directory from the manifest.
# ----------------------------------------------------------------------

probe_metadata = dict(manifest.metadata)

probe_metadata["source_path"] = str(SOURCE)

probe_manifest = replace(
    manifest,
    destination_directory=destination,
    metadata=probe_metadata,
)

print()
print("-" * 72)
print("Probe manifest")
print("-" * 72)

print(
    "source_path metadata :",
    probe_manifest.get_metadata("source_path"),
)

print(
    "destination_directory:",
    probe_manifest.destination_directory,
)


# ----------------------------------------------------------------------
# 5. Importer selection
# ----------------------------------------------------------------------

importer = LocalFileImporter()

supported = importer.supports(probe_manifest)

print()
print("-" * 72)
print("Importer selection")
print("-" * 72)

print("supports(manifest) :", supported)

assert supported is True

print("Importer selection : PASS")


# ----------------------------------------------------------------------
# 6. Execute existing LocalFileImporter
# ----------------------------------------------------------------------

try:

    result = importer.download(probe_manifest)

    print()
    print("-" * 72)
    print("AcquisitionResult")
    print("-" * 72)

    print("result type :", type(result).__name__)
    print("success     :", result.success)
    print("message     :", result.message)
    print("started_at  :", result.started_at)
    print("completed_at:", result.completed_at)
    print("duration    :", result.duration_seconds)

    print()
    print("downloaded_files :", result.downloaded_files)
    print("extracted_files  :", result.extracted_files)
    print("bytes_downloaded :", result.bytes_downloaded)

    print()
    print("checksum_verified :", result.checksum_verified)
    print("license_verified  :", result.license_verified)
    print("normalized        :", result.normalized)
    print("imported          :", result.imported)

    print()
    print("warnings:")
    for warning in result.warnings:
        print("  -", warning)

    print()
    print("errors:")
    for error in result.errors:
        print("  -", error)

    print()
    print("metadata:")

    if result.metadata:
        for key, value in sorted(result.metadata.items()):
            print(f"  {key} = {value!r}")
    else:
        print("  <empty>")

    # --------------------------------------------------------------
    # 7. Diagnostic failure handling
    # --------------------------------------------------------------

    if not result.success:

        print()
        print("=" * 72)
        print("LOCAL IMPORTER RETURNED success=False")
        print("=" * 72)

        print()
        print("This is a runtime contract failure, not an audit")
        print("bootstrap failure.")
        print()
        print("The diagnostic information above is authoritative.")
        print()
        print("No production file will be modified by this audit.")

        raise AssertionError(
            "LocalFileImporter returned AcquisitionResult.success=False. "
            "See message/errors/metadata above."
        )

    print()
    print("LocalFileImporter execution : PASS")


    # ------------------------------------------------------------------
    # 8. Temporary output verification
    # ------------------------------------------------------------------

    print()
    print("-" * 72)
    print("Temporary destination verification")
    print("-" * 72)

    copied_files = [
        path
        for path in probe_root.rglob("*")
        if path.is_file()
    ]

    print("files produced :", len(copied_files))

    for path in copied_files:
        print(
            f"{path} | "
            f"{path.stat().st_size} bytes | "
            f"{sha256(path)}"
        )

    assert copied_files, (
        "LocalFileImporter reported success but produced no files."
    )

    matching = [
        path
        for path in copied_files
        if path.name == SOURCE.name
    ]

    assert matching, (
        "LocalFileImporter reported success but "
        "amarakosha.txt was not found."
    )

    copied = matching[0]

    assert copied.stat().st_size == EXPECTED_SIZE
    assert sha256(copied) == EXPECTED_SHA256

    print()
    print("destination file : PASS")
    print("destination size : PASS")
    print("destination hash : PASS")


finally:

    # --------------------------------------------------------------
    # 9. Cleanup
    # --------------------------------------------------------------

    shutil.rmtree(
        probe_root,
        ignore_errors=True,
    )


# ----------------------------------------------------------------------
# 10. Verify canonical source was never modified
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("Canonical source preservation")
print("-" * 72)

assert SOURCE.is_file()
assert SOURCE.stat().st_size == EXPECTED_SIZE
assert sha256(SOURCE) == EXPECTED_SHA256

print("source exists   : PASS")
print("source size     : PASS")
print("source checksum : PASS")


# ----------------------------------------------------------------------
# Final
# ----------------------------------------------------------------------

print()
print("=" * 72)
print("RESULT: PASS — LocalFileImporter successfully reproduced")
print("the verified Amarakośa artifact in a temporary destination.")
print("No production files modified.")
print("=" * 72)
