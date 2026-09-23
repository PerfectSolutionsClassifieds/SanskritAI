
from pathlib import Path
import inspect
import sys

REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from SanskritAI.acquisition.downloaders.local_file_importer import (
    LocalFileImporter,
)
from SanskritAI.acquisition.acquirers.default_source_acquirer import (
    DefaultSourceAcquirer,
)
from SanskritAI.acquisition.models.acquisition_manifest import (
    AcquisitionManifest,
)


print("=" * 72)
print("13R-8F-1 — Local acquisition dispatch contract audit")
print("=" * 72)


# ----------------------------------------------------------------------
# LocalFileImporter
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("LocalFileImporter public contract")
print("-" * 72)

print("constructor :", inspect.signature(LocalFileImporter))

for name in (
    "supports",
    "download",
    "validate_destination",
    "finalize_result",
):
    method = getattr(LocalFileImporter, name, None)

    if method is not None:
        print()
        print(f"### {name}")
        try:
            print(inspect.signature(method))
        except (TypeError, ValueError):
            pass

        print(inspect.getsource(method))


# ----------------------------------------------------------------------
# Private copy methods
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("LocalFileImporter copy implementation")
print("-" * 72)

for name in (
    "_copy_file",
    "_copy_directory",
):
    method = getattr(LocalFileImporter, name, None)

    if method is not None:
        print()
        print(f"### {name}")
        print(inspect.signature(method))
        print(inspect.getsource(method))


# ----------------------------------------------------------------------
# DefaultSourceAcquirer constructor and instance state
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("DefaultSourceAcquirer contract")
print("-" * 72)

print(
    "constructor :",
    inspect.signature(DefaultSourceAcquirer),
)

acquirer = DefaultSourceAcquirer()

print()
print("instance attributes:")
for key, value in vars(acquirer).items():
    print(f"  {key} = {value!r}")


# ----------------------------------------------------------------------
# Check whether DefaultSourceAcquirer already owns an importer-like
# dependency or extension point.
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("Potential dispatch extension points")
print("-" * 72)

for name in sorted(dir(acquirer)):
    if name.startswith("__"):
        continue

    try:
        value = getattr(acquirer, name)
    except Exception:
        continue

    if callable(value):
        print(f"METHOD    {name}")
    else:
        print(f"ATTRIBUTE {name} = {value!r}")


# ----------------------------------------------------------------------
# AcquisitionManifest helpers relevant to local dispatch
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("AcquisitionManifest local-dispatch helpers")
print("-" * 72)

for name in (
    "all_urls",
    "has_urls",
    "requires_download",
    "get_metadata",
    "set_metadata",
):
    value = getattr(AcquisitionManifest, name, None)

    if value is not None:
        print()
        print(f"### {name}")

        try:
            if callable(value):
                print(inspect.signature(value))
                print(inspect.getsource(value))
            else:
                print(value)
        except Exception as exc:
            print(f"<inspection failed: {exc}>")


# ----------------------------------------------------------------------
# Decision
# ----------------------------------------------------------------------

print()
print("=" * 72)
print("13R-8F-1 decision")
print("=" * 72)
print()
print("This audit is read-only.")
print("No production files modified.")
print()
print(
    "Use the existing LocalFileImporter if the contract supports "
    "generic delegation from DefaultSourceAcquirer."
)
print("=" * 72)
