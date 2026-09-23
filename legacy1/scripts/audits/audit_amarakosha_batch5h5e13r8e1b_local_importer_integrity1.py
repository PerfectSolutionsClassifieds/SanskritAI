from pathlib import Path
import hashlib
import shutil
import sys
import tempfile

REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from SanskritAI.acquisition.downloaders.local_file_importer import LocalFileImporter
from SanskritAI.acquisition.sources.amarakosha_manifest import create_amarakosha_manifest


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

assert SOURCE.is_file()
assert SOURCE.stat().st_size == EXPECTED_SIZE
assert sha256(SOURCE) == EXPECTED_SHA256

print("Canonical source integrity : PASS")

manifest = create_amarakosha_manifest()

probe_root = Path(tempfile.mkdtemp(prefix="sanskritai_amarakosha_import_"))
destination = probe_root / "destination"
destination.mkdir(parents=True, exist_ok=True)

# LocalFileImporter consumes source_path from manifest metadata.
# Keep the production manifest untouched.
probe_manifest = manifest
probe_manifest.metadata["source_path"] = str(SOURCE)

importer = LocalFileImporter()

print()
print("-" * 72)
print("Importer selection")
print("-" * 72)

supported = importer.supports(probe_manifest)

print("supports(manifest) :", supported)

assert supported is True

print("Importer selection : PASS")

try:
    # Use the existing importer contract.
    result = importer.download(
        probe_manifest,
    )

    print()
    print("-" * 72)
    print("AcquisitionResult")
    print("-" * 72)

    print("result type :", type(result).__name__)
    print("success     :", getattr(result, "success", None))

    assert getattr(result, "success", False) is True

    # The importer contract may expose the final path under a
    # source-specific result field. Inspect without assuming names.
    print("result attributes:")
    for name in sorted(dir(result)):
        if name.startswith("_"):
            continue

        try:
            value = getattr(result, name)
        except Exception:
            continue

        if not callable(value):
            print(f"  {name} = {value!r}")

    # Search the temporary probe directory for the copied artifact.
    copied_files = [
        p for p in probe_root.rglob("*")
        if p.is_file()
    ]

    print()
    print("-" * 72)
    print("Temporary destination verification")
    print("-" * 72)

    for path in copied_files:
        print(
            f"{path} | "
            f"{path.stat().st_size} bytes | "
            f"{sha256(path)}"
        )

    assert copied_files, "Importer reported success but no output file exists."

    matching = [
        p for p in copied_files
        if p.name == SOURCE.name
    ]

    assert matching, "amarakosha.txt was not copied to probe destination."

    copied = matching[0]

    assert copied.stat().st_size == EXPECTED_SIZE
    assert sha256(copied) == EXPECTED_SHA256

    print("destination file : PASS")
    print("destination size : PASS")
    print("destination hash : PASS")

finally:
    shutil.rmtree(probe_root, ignore_errors=True)

print()
print("Canonical source still exists :", SOURCE.is_file())
print("Canonical source unchanged    :", SOURCE.stat().st_size == EXPECTED_SIZE)

assert SOURCE.is_file()
assert SOURCE.stat().st_size == EXPECTED_SIZE
assert sha256(SOURCE) == EXPECTED_SHA256

print()
print("=" * 72)
print("RESULT: PASS — LocalFileImporter successfully reproduced")
print("the verified Amarakośa artifact in a temporary destination.")
print("No production files modified.")
print("=" * 72)
