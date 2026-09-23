
from pathlib import Path
import ast
import inspect
import sys

REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))


print("=" * 72)
print("13R-8F-0 — Generic local acquisition dispatch boundary audit")
print("=" * 72)

ACQUISITION_ROOT = REPO_ROOT / "acquisition"

production_files = [
    p for p in ACQUISITION_ROOT.rglob("*.py")
    if not p.name.endswith("__pycache__.py")
    and not any(
        part == "__pycache__"
        for part in p.parts
    )
    and not any(
        p.stem.endswith(f"_{i}")
        for i in range(1, 20)
    )
    and not any(
        p.stem.endswith(str(i))
        for i in range(1, 20)
    )
]


print()
print("Production acquisition files :", len(production_files))


# ----------------------------------------------------------------------
# AST reference scan
# ----------------------------------------------------------------------

TARGETS = {
    "LocalFileImporter",
    "ImporterRegistry",
    "ImportManager",
    "DefaultSourceAcquirer",
    "SourceAcquirer",
    "AcquisitionPipeline",
    "AcquisitionService",
    "DefaultAcquisitionService",
    "source_path",
    "destination_directory",
    "all_urls",
    "requires_download",
}


references = {
    name: []
    for name in TARGETS
}


for path in production_files:

    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception:
        continue

    for node in ast.walk(tree):

        if isinstance(node, ast.Name):
            if node.id in references:
                references[node.id].append(
                    (str(path.relative_to(REPO_ROOT)), node.lineno)
                )

        elif isinstance(node, ast.Attribute):
            if node.attr in references:
                references[node.attr].append(
                    (str(path.relative_to(REPO_ROOT)), node.lineno)
                )

        elif isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                for target in ("source_path",):
                    if target in node.value:
                        references[target].append(
                            (
                                str(path.relative_to(REPO_ROOT)),
                                node.lineno,
                            )
                        )


print()
print("-" * 72)
print("Reference evidence")
print("-" * 72)

for target in sorted(TARGETS):

    matches = references[target]

    print()
    print(f"{target} : {len(matches)}")

    for path, line in matches[:20]:
        print(f"  {path}:{line}")


# ----------------------------------------------------------------------
# Runtime imports
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("Runtime imports")
print("-" * 72)

from SanskritAI.acquisition.downloaders.local_file_importer import (
    LocalFileImporter,
)

from SanskritAI.acquisition.acquirers.default_source_acquirer import (
    DefaultSourceAcquirer,
)

from SanskritAI.acquisition.pipelines.acquisition_pipeline import (
    AcquisitionPipeline,
)

from SanskritAI.acquisition.services.default_acquisition_service import (
    DefaultAcquisitionService,
)

print("LocalFileImporter        : PASS")
print("DefaultSourceAcquirer   : PASS")
print("AcquisitionPipeline      : PASS")
print("DefaultAcquisitionService: PASS")


# ----------------------------------------------------------------------
# Class/method contract
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("Runtime contracts")
print("-" * 72)

classes = [
    LocalFileImporter,
    DefaultSourceAcquirer,
    AcquisitionPipeline,
    DefaultAcquisitionService,
]

for cls in classes:

    print()
    print(cls.__name__)
    print("constructor :", inspect.signature(cls))

    for method_name in (
        "supports",
        "download",
        "acquire",
        "run",
    ):
        method = getattr(cls, method_name, None)

        if method is not None:

            try:
                print(
                    f"  {method_name}{inspect.signature(method)}"
                )
            except (TypeError, ValueError):
                print(f"  {method_name}")


# ----------------------------------------------------------------------
# SourceAcquirer dispatch inspection
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("DefaultSourceAcquirer.acquire source")
print("-" * 72)

print(
    inspect.getsource(
        DefaultSourceAcquirer.acquire
    )
)


print()
print("-" * 72)
print("DefaultSourceAcquirer local/download helpers")
print("-" * 72)

for method_name in (
    "_validate_manifest",
    "_download_from_sources",
    "_download_one",
    "_copy_local_file",
):

    method = getattr(DefaultSourceAcquirer, method_name, None)

    if method is not None:

        print()
        print(f"### {method_name}")
        print(inspect.getsource(method))


# ----------------------------------------------------------------------
# LocalFileImporter implementation
# ----------------------------------------------------------------------

print()
print("-" * 72)
print("LocalFileImporter implementation")
print("-" * 72)

for method_name in (
    "supports",
    "download",
):

    method = getattr(LocalFileImporter, method_name)

    print()
    print(f"### {method_name}")
    print(inspect.getsource(method))


# ----------------------------------------------------------------------
# Decision
# ----------------------------------------------------------------------

local_refs = references["LocalFileImporter"]

print()
print("=" * 72)

if local_refs:
    print("LocalFileImporter references detected.")
else:
    print("No LocalFileImporter orchestration references detected.")

print()
print("13R-8F-0 decision:")
print()
print("Do not modify production code in this audit.")
print("Identify the smallest existing generic dispatch boundary.")
print("=" * 72)
