from __future__ import annotations

from pathlib import Path
import inspect
import sys


ROOT = Path("/content/SanskritAI")

if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))


print("=" * 72)
print("13R-8C — Amarakośa LocalFileImporter contract audit")
print("=" * 72)
print(f"Repository root : {ROOT}")


# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------

from SanskritAI.acquisition.downloaders.base_downloader import (
    BaseDownloader,
)

from SanskritAI.acquisition.downloaders.local_file_importer import (
    LocalFileImporter,
)

from SanskritAI.acquisition.models.acquisition_result import (
    AcquisitionResult,
)

from SanskritAI.acquisition.sources.amarakosha_manifest import (
    create_amarakosha_manifest,
)


print()
print("-" * 72)
print("Imports")
print("-" * 72)

print("BaseDownloader       : PASS")
print("LocalFileImporter    : PASS")
print("AcquisitionResult    : PASS")
print("Amarakośa manifest   : PASS")


# ---------------------------------------------------------------------
# Instantiate
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Instantiation")
print("-" * 72)

importer = LocalFileImporter()

print(f"instance : {importer!r}")
print(f"type     : {type(importer).__name__}")


# ---------------------------------------------------------------------
# Full BaseDownloader contract
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("BaseDownloader methods")
print("-" * 72)

for name in (
    "supports",
    "download",
    "prepare_directory",
    "validate_destination",
    "destination_file",
    "remove_existing",
    "finalize_result",
):
    method = getattr(BaseDownloader, name, None)

    print()
    print(f"--- {name} ---")

    if method is None:
        print("MISSING")
        continue

    try:
        print(inspect.getsource(method))
    except Exception as exc:
        print(f"source unavailable: {exc}")


# ---------------------------------------------------------------------
# Full LocalFileImporter contract
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("LocalFileImporter methods")
print("-" * 72)

for name in (
    "supports",
    "download",
    "_copy_file",
    "_copy_directory",
):
    method = getattr(LocalFileImporter, name, None)

    print()
    print(f"--- {name} ---")

    if method is None:
        print("MISSING")
        continue

    try:
        print(inspect.getsource(method))
    except Exception as exc:
        print(f"source unavailable: {exc}")


# ---------------------------------------------------------------------
# Amarakośa manifest
# ---------------------------------------------------------------------

manifest = create_amarakosha_manifest()

print()
print("-" * 72)
print("Amarakośa manifest")
print("-" * 72)

print(f"source_id          : {manifest.source.source_id}")
print(f"source.local_path  : {manifest.source.local_path}")
print(f"destination        : {manifest.destination_directory}")
print(f"expected_filename  : {manifest.expected_filename}")
print(f"expected_size      : {manifest.expected_size}")
print(f"checksum           : {manifest.checksum}")
print(f"overwrite_existing : {manifest.overwrite_existing}")


# ---------------------------------------------------------------------
# Current LocalFileImporter selection contract
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Current supports() contract")
print("-" * 72)

print(
    "supports(manifest) before source_path metadata :",
    importer.supports(manifest),
)

print(
    "source_path metadata before modification       :",
    manifest.get_metadata("source_path"),
)


# ---------------------------------------------------------------------
# Read-only cloned metadata contract
#
# We do NOT modify the production manifest object.
# We create a fresh manifest and attach the local source path only
# to the fresh manifest's metadata.
# ---------------------------------------------------------------------

probe_manifest = create_amarakosha_manifest()

probe_manifest.set_metadata(
    "source_path",
    str(probe_manifest.source.local_path),
)

print()
print("-" * 72)
print("Local source-path compatibility probe")
print("-" * 72)

print(
    "source_path metadata :",
    probe_manifest.get_metadata("source_path"),
)

print(
    "supports(probe)      :",
    importer.supports(probe_manifest),
)


# ---------------------------------------------------------------------
# Destination calculation
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Destination calculation")
print("-" * 72)

source_path = Path(
    probe_manifest.get_metadata("source_path")
)

destination_directory = Path(
    probe_manifest.destination_directory
)

expected_filename = probe_manifest.expected_filename

expected_destination = (
    destination_directory / expected_filename
)

print(f"source      : {source_path}")
print(f"destination : {expected_destination}")

try:
    same_file = (
        source_path.resolve()
        == expected_destination.resolve()
    )
except FileNotFoundError:
    same_file = (
        source_path.absolute()
        == expected_destination.absolute()
    )

print(f"same file   : {same_file}")


# ---------------------------------------------------------------------
# Safety decision
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Execution safety")
print("-" * 72)

if same_file:
    print(
        "IMPORTANT: LocalFileImporter source and destination "
        "resolve to the same file."
    )

    print(
        "No LocalFileImporter.download() execution will be attempted."
    )

else:
    print(
        "Source and destination differ."
    )

    print(
        "A runtime probe may be possible after checksum semantics "
        "are independently verified."
    )


# ---------------------------------------------------------------------
# AcquisitionResult contract
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("AcquisitionResult contract")
print("-" * 72)

for name in (
    "mark_success",
    "add_error",
    "add_warning",
    "add_downloaded_file",
    "finalize",
):
    method = getattr(AcquisitionResult, name, None)

    print()
    print(f"--- {name} ---")

    if method is None:
        print("MISSING")
        continue

    try:
        print(inspect.getsource(method))
    except Exception as exc:
        print(f"source unavailable: {exc}")


# ---------------------------------------------------------------------
# Final decision
# ---------------------------------------------------------------------

print()
print("=" * 72)
print("13R-8C decision")
print("=" * 72)

print(
    "PASS — LocalFileImporter contract inspected without "
    "executing a copy."
)

print(
    "No production files were modified."
)

print(
    "No Amarakośa-specific acquisition class was created."
)
