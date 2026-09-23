from __future__ import annotations

from pathlib import Path
import inspect
import sys


ROOT = Path("/content/SanskritAI")

if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))


print("=" * 72)
print("13R-8B — Amarakośa acquisition runtime contract inspection")
print("=" * 72)
print(f"Repository root : {ROOT}")


# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Runtime imports")
print("-" * 72)

try:
    from SanskritAI.acquisition.acquirers.default_source_acquirer import (
        DefaultSourceAcquirer,
    )
    print("DefaultSourceAcquirer : PASS")
except Exception as exc:
    print(f"DefaultSourceAcquirer : FAIL — {exc}")
    raise

try:
    from SanskritAI.acquisition.pipelines.acquisition_pipeline import (
        AcquisitionPipeline,
    )
    print("AcquisitionPipeline : PASS")
except Exception as exc:
    print(f"AcquisitionPipeline : FAIL — {exc}")
    raise

try:
    from SanskritAI.acquisition.services.default_acquisition_service import (
        DefaultAcquisitionService,
    )
    print("DefaultAcquisitionService : PASS")
except Exception as exc:
    print(f"DefaultAcquisitionService : FAIL — {exc}")
    raise

try:
    from SanskritAI.acquisition.downloaders.local_file_importer import (
        LocalFileImporter,
    )
    print("LocalFileImporter : PASS")
except Exception as exc:
    print(f"LocalFileImporter : FAIL — {exc}")
    raise


# ---------------------------------------------------------------------
# Amarakośa manifest
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Amarakośa manifest")
print("-" * 72)

from SanskritAI.acquisition.sources.amarakosha_manifest import (
    create_amarakosha_manifest,
)

manifest = create_amarakosha_manifest()

print(f"manifest_id        : {manifest.manifest_id}")
print(f"source_id          : {manifest.source.source_id}")
print(f"source.local_path  : {manifest.source.local_path}")
print(f"destination        : {manifest.destination_directory}")
print(f"expected_filename  : {manifest.expected_filename}")
print(f"expected_size      : {manifest.expected_size}")
print(f"checksum           : {manifest.checksum}")
print(f"urls               : {manifest.urls}")
print(f"mirrors            : {manifest.mirrors}")
print(f"requires_download  : {manifest.requires_download}")
print(
    "requires_checksum_validation : "
    f"{manifest.requires_checksum_validation}"
)
print(f"metadata           : {manifest.metadata}")


# ---------------------------------------------------------------------
# Inspect DefaultSourceAcquirer source
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("DefaultSourceAcquirer.acquire() source")
print("-" * 72)

print(
    inspect.getsource(
        DefaultSourceAcquirer.acquire
    )
)


print()
print("-" * 72)
print("DefaultSourceAcquirer._validate_manifest() source")
print("-" * 72)

print(
    inspect.getsource(
        DefaultSourceAcquirer._validate_manifest
    )
)


print()
print("-" * 72)
print("DefaultSourceAcquirer._prepare_destination() source")
print("-" * 72)

print(
    inspect.getsource(
        DefaultSourceAcquirer._prepare_destination
    )
)


print()
print("-" * 72)
print("DefaultSourceAcquirer._download_from_sources() source")
print("-" * 72)

print(
    inspect.getsource(
        DefaultSourceAcquirer._download_from_sources
    )
)


print()
print("-" * 72)
print("DefaultSourceAcquirer._download_one() source")
print("-" * 72)

print(
    inspect.getsource(
        DefaultSourceAcquirer._download_one
    )
)


print()
print("-" * 72)
print("DefaultSourceAcquirer._copy_local_file() source")
print("-" * 72)

print(
    inspect.getsource(
        DefaultSourceAcquirer._copy_local_file
    )
)


print()
print("-" * 72)
print("DefaultSourceAcquirer._verify_checksum() source")
print("-" * 72)

print(
    inspect.getsource(
        DefaultSourceAcquirer._verify_checksum
    )
)


# ---------------------------------------------------------------------
# Inspect LocalFileImporter
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("LocalFileImporter contract")
print("-" * 72)

print(
    inspect.getsource(
        LocalFileImporter.supports
    )
)

print(
    inspect.getsource(
        LocalFileImporter.download
    )
)

# ---------------------------------------------------------------------
# Inspect pipeline
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("AcquisitionPipeline.acquire()")
print("-" * 72)

print(
    inspect.getsource(
        AcquisitionPipeline.acquire
    )
)


print()
print("-" * 72)
print("AcquisitionPipeline.run()")
print("-" * 72)

print(
    inspect.getsource(
        AcquisitionPipeline.run
    )
)


# ---------------------------------------------------------------------
# Inspect service
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("DefaultAcquisitionService.acquire()")
print("-" * 72)

print(
    inspect.getsource(
        DefaultAcquisitionService.acquire
    )
)


print()
print("-" * 72)
print("DefaultAcquisitionService.run()")
print("-" * 72)

print(
    inspect.getsource(
        DefaultAcquisitionService.run
    )
)


# ---------------------------------------------------------------------
# Constructor signatures
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Runtime constructor signatures")
print("-" * 72)

print(
    "DefaultSourceAcquirer:",
    inspect.signature(DefaultSourceAcquirer),
)

print(
    "AcquisitionPipeline:",
    inspect.signature(AcquisitionPipeline),
)

print(
    "DefaultAcquisitionService:",
    inspect.signature(DefaultAcquisitionService),
)

print(
    "LocalFileImporter:",
    inspect.signature(LocalFileImporter),
)


# ---------------------------------------------------------------------
# Safety check before actual execution
# ---------------------------------------------------------------------

print()
print("-" * 72)
print("Safety assessment")
print("-" * 72)

artifact = manifest.source.local_path
destination = manifest.destination_directory
expected = manifest.expected_filename

print(f"artifact exists : {artifact.exists() if artifact else False}")
print(f"artifact path   : {artifact}")
print(f"destination     : {destination}")
print(f"expected path   : {destination / expected if destination and expected else None}")

if artifact is not None and destination is not None and expected:
    target = destination / expected

    if artifact.resolve() == target.resolve():
        print()
        print(
            "IMPORTANT: source artifact and expected destination "
            "resolve to the SAME FILE."
        )
        print(
            "No acquisition execution should be attempted until "
            "the runtime's same-file behavior is explicitly understood."
        )
    else:
        print()
        print(
            "Source artifact and expected destination are different."
        )


print()
print("=" * 72)
print("13R-8B decision")
print("=" * 72)

print(
    "PASS — runtime contract inspected read-only."
)

print(
    "No acquisition was executed and no production files were modified."
)
