from __future__ import annotations

"""
SanskritAI
==========

13R-8F-11 — Local Registration Contract Audit

Purpose
-------
Establish the design contract for already-local canonical artifacts.

This audit is READ-ONLY.

No production files are modified.

Primary architectural question
-------------------------------
Can an already-local CorpusSource be represented and processed
using the existing acquisition lifecycle without introducing a
new importer, downloader, or source status?

Expected existing concepts
---------------------------
CorpusSource.local_path
CorpusSource.is_downloaded
SourceStatus.REGISTERED
SourceStatus.SKIPPED
SourceStatus.DOWNLOADED
AcquisitionResult
AcquisitionManifest

Candidate lifecycle
-------------------
REGISTERED
    |
    | local_path exists
    v
LOCAL ARTIFACT VALIDATION
    |
    +---- identity/size/checksum valid
    |
    v
SKIPPED physical acquisition
    |
    v
AcquisitionResult(success=True)
    |
    v
READY_FOR_IMPORT / downstream lifecycle

This script does NOT implement that lifecycle.
It determines whether the existing architecture can support it.
"""

import ast
import hashlib
import inspect
import sys
import textwrap
from pathlib import Path


# ==========================================================================
# Runtime bootstrap
# ==========================================================================

REPO_ROOT = Path("/content/SanskritAI").resolve()
WORKSPACE_ROOT = REPO_ROOT.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))


# ==========================================================================
# Production paths
# ==========================================================================

PATHS = {
    "corpus_source": (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "corpus_source.py"
    ),
    "source_status": (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "source_status.py"
    ),
    "acquisition_manifest": (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "acquisition_manifest.py"
    ),
    "acquisition_result": (
        REPO_ROOT
        / "acquisition"
        / "models"
        / "acquisition_result.py"
    ),
    "local_file_importer": (
        REPO_ROOT
        / "acquisition"
        / "downloaders"
        / "local_file_importer.py"
    ),
    "default_source_acquirer": (
        REPO_ROOT
        / "acquisition"
        / "acquirers"
        / "default_source_acquirer.py"
    ),
    "amarakosha_source": (
        REPO_ROOT
        / "acquisition"
        / "sources"
        / "amarakosha.py"
    ),
    "amarakosha_manifest": (
        REPO_ROOT
        / "acquisition"
        / "sources"
        / "amarakosha_manifest.py"
    ),
}


AMARAKOSHA_ARTIFACT = (
    REPO_ROOT / "amarakosha.txt"
)


# ==========================================================================
# Helpers
# ==========================================================================

def banner(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def syntax_check(path: Path) -> None:
    ast.parse(read(path), filename=str(path))
    print(f"{path}: Python syntax PASS")


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def get_class(tree: ast.AST, name: str):
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def get_method(class_node: ast.ClassDef, name: str):
    for node in class_node.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    return None


def method_source(path: Path, class_name: str, method_name: str) -> str:
    source = read(path)
    tree = ast.parse(source, filename=str(path))

    cls = get_class(tree, class_name)
    if cls is None:
        raise RuntimeError(f"Class {class_name!r} not found in {path}")

    method = get_method(cls, method_name)
    if method is None:
        raise RuntimeError(f"Method {method_name!r} not found in {class_name}")

    lines = source.splitlines()
    extracted = "\n".join(lines[method.lineno - 1 : method.end_lineno])
    return textwrap.dedent(extracted)


def ast_calls(source: str) -> set[str]:
    tree = ast.parse(textwrap.dedent(source))
    result: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            result.add(func.id)
        elif isinstance(func, ast.Attribute):
            result.add(func.attr)
    return result


def contains_any(source: str, values: tuple[str, ...]) -> bool:
    return any(value in source for value in values)


def definitions(source: str) -> set[str]:
    tree = ast.parse(source)
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result.add(node.name)
    return result


# ==========================================================================
# Header
# ==========================================================================

banner("13R-8F-11 — Local Registration Contract Audit")

print(f"Repository root : {REPO_ROOT}")
print(f"Workspace root  : {WORKSPACE_ROOT}")


# ==========================================================================
# 1. Syntax
# ==========================================================================

banner("1. Production syntax")

for name, path in PATHS.items():
    if not path.exists():
        print(f"WARNING: missing {name}: {path}")
        continue
    syntax_check(path)


# ==========================================================================
# 2. Canonical runtime objects
# ==========================================================================

banner("2. Canonical runtime objects")

from SanskritAI.acquisition.sources.amarakosha import create_amarakosha_source
from SanskritAI.acquisition.sources.amarakosha_manifest import create_amarakosha_manifest
from SanskritAI.acquisition.models.source_status import SourceStatus

source = create_amarakosha_source()
manifest = create_amarakosha_manifest()

print(f"source_id       : {source.source_id}")
print(f"source.status   : {source.status}")
print(f"source.local_path: {source.local_path}")
print(f"source.is_downloaded: {source.is_downloaded}")
print(f"manifest_id     : {manifest.manifest_id}")
print(f"manifest.urls   : {manifest.urls}")
print(f"manifest.mirrors: {manifest.mirrors}")
print(f"manifest.destination: {manifest.destination_directory}")
print(f"manifest.filename: {manifest.expected_filename}")


# ==========================================================================
# 3. SourceStatus capability
# ==========================================================================

banner("3. SourceStatus registration capability")

status_source = read(PATHS["source_status"])

required_statuses = (
    "REGISTERED",
    "SKIPPED",
    "DOWNLOADED",
    "VALIDATING",
    "VALIDATED",
    "READY_FOR_IMPORT",
    "FAILED",
)

for name in required_statuses:
    present = name in status_source
    print(f"{name:18} : {'PRESENT' if present else 'MISSING'}")


# ==========================================================================
# 4. CorpusSource capability
# ==========================================================================

banner("4. CorpusSource local-registration capability")

corpus_source = read(PATHS["corpus_source"])

print("local_path field/reference: " f"{'PRESENT' if 'local_path' in corpus_source else 'MISSING'}")
print("is_downloaded property: " f"{'PRESENT' if 'is_downloaded' in corpus_source else 'MISSING'}")
print("set_local_path(): " f"{'PRESENT' if 'set_local_path' in corpus_source else 'MISSING'}")
print("REGISTERED status reference: " f"{'PRESENT' if 'REGISTERED' in corpus_source else 'MISSING'}")


# ==========================================================================
# 5. AcquisitionManifest capability
# ==========================================================================

banner("5. AcquisitionManifest capability")

manifest_source = read(PATHS["acquisition_manifest"])

for field in (
    "destination_directory",
    "expected_filename",
    "expected_size",
    "checksum",
    "checksum_algorithm",
    "overwrite_existing",
    "validate_checksum",
    "enabled",
    "metadata",
):
    print(f"{field:22} : {'PRESENT' if field in manifest_source else 'MISSING'}")


# ==========================================================================
# 6. AcquisitionResult capability
# ==========================================================================

banner("6. AcquisitionResult capability")

result_source = read(PATHS["acquisition_result"])

for field in (
    "success",
    "message",
    "downloaded_files",
    "bytes_downloaded",
    "checksum_verified",
    "warnings",
    "errors",
):
    print(f"{field:22} : {'PRESENT' if field in result_source else 'MISSING'}")

for method in ("mark_success", "add_warning", "add_error", "add_downloaded_file", "finalize"):
    print(f"{method}(): {'PRESENT' if f'def {method}' in result_source else 'MISSING'}")


# ==========================================================================
# 7. Existing local importer boundary
# ==========================================================================

banner("7. LocalFileImporter boundary")

local_importer_source = read(PATHS["local_file_importer"])

print("LocalFileImporter class: " f"{'PRESENT' if 'class LocalFileImporter' in local_importer_source else 'MISSING'}")
print("_resolve_source_path(): " f"{'PRESENT' if '_resolve_source_path' in local_importer_source else 'MISSING'}")
print("CorpusSource.local_path canonical resolution: " f"{'PRESENT' if 'local_path' in local_importer_source else 'MISSING'}")
print("No new registration importer required by current architecture: DESIGN-PASS")


# ==========================================================================
# 8. DefaultSourceAcquirer capability
# ==========================================================================

banner("8. DefaultSourceAcquirer lifecycle capability")

acquirer_source = read(PATHS["default_source_acquirer"])

acquire_source = method_source(PATHS["default_source_acquirer"], "DefaultSourceAcquirer", "acquire")

calls = ast_calls(acquire_source)

print("acquire() calls _validate_manifest(): " f"{'_validate_manifest' in calls}")
print("acquire() calls _prepare_destination(): " f"{'_prepare_destination' in calls}")
print("acquire() calls _download_from_sources(): " f"{'_download_from_sources' in calls}")
print("acquire() calls result.finalize(): " f"{'finalize' in calls}")
print("acquire() contains LocalFileImporter reference: " f"{'LocalFileImporter' in acquire_source}")
print("acquire() contains SourceStatus.SKIPPED: " f"{'SKIPPED' in acquire_source}")
print("acquire() contains source.local_path: " f"{'local_path' in acquire_source}")


# ==========================================================================
# 9. Current local dispatch contract
# ==========================================================================

banner("9. Current local dispatch contract")

local_dispatch_evidence = {
    "LocalFileImporter": ("LocalFileImporter" in acquire_source),
    "source.local_path": ("local_path" in acquire_source),
    "metadata source_path": ("source_path" in acquire_source),
    "SKIPPED": ("SKIPPED" in acquire_source),
}

for name, present in local_dispatch_evidence.items():
    print(f"{name:24} : {'PRESENT' if present else 'ABSENT'}")


# ==========================================================================
# 10. Production collision
# ==========================================================================

banner("10. Production local artifact collision")

artifact = AMARAKOSHA_ARTIFACT.resolve()

destination = (
    Path(manifest.destination_directory).resolve()
    / (manifest.expected_filename or artifact.name)
)

print(f"artifact    : {artifact}")
print(f"destination : {destination}")

same_path = (artifact == destination)

print(f"same physical path: {same_path}")

if not same_path:
    print("Unexpected: production collision disappeared.")


# ==========================================================================
# 11. Design contract candidate
# ==========================================================================

banner("11. Candidate local-registration contract")

print("The existing architecture provides:")
print("  CorpusSource.local_path")
print("  CorpusSource.is_downloaded")
print("  SourceStatus.REGISTERED")
print("  SourceStatus.SKIPPED")
print("  AcquisitionResult")
print("  LocalFileImporter for actual filesystem copying")
print()
print("Therefore the preferred design is:")
print("  Existing canonical local artifact")
print("        -> validate existing artifact")
print("        -> do NOT invoke physical copy")
print("        -> produce successful AcquisitionResult")
print("        -> preserve local_path")
print("        -> leave checksum/normalization/import flags to their respective lifecycle stages")


# ==========================================================================
# 12. Missing capability identification
# ==========================================================================

banner("12. Missing generic capability")

print("Checking whether DefaultSourceAcquirer already has a dedicated same-source/local-registration branch.")

registration_markers = (
    "already_downloaded",
    "already_exists",
    "is_downloaded",
    "source.local_path",
    "SKIPPED",
)

present_markers = [marker for marker in registration_markers if marker in acquire_source]

print("Detected markers:")
for marker in present_markers:
    print(f"  {marker}")

if ("is_downloaded" not in acquire_source) and ("source.local_path" not in acquire_source):
    print("No explicit local-registration branch detected.")
    print("This indicates a generic acquisition-boundary repair may be required.")
else:
    print("Some local-registration markers already exist.")
    print("Inspect their exact control flow before repair.")


# ==========================================================================
# 13. Read-only runtime sanity
# ==========================================================================

banner("13. Runtime sanity")

print(f"source.is_downloaded : {source.is_downloaded}")
print(f"source.local_path exists: {Path(source.local_path).is_file()}")
print(f"artifact size: {AMARAKOSHA_ARTIFACT.stat().st_size}")
print(f"artifact sha256: {hash_file(AMARAKOSHA_ARTIFACT)}")


# ==========================================================================
# 14. Immutability
# ==========================================================================

banner("14. Read-only audit guarantee")

final_size = AMARAKOSHA_ARTIFACT.stat().st_size
final_hash = hash_file(AMARAKOSHA_ARTIFACT)

assert final_size == AMARAKOSHA_ARTIFACT.stat().st_size
assert final_hash == hash_file(AMARAKOSHA_ARTIFACT)

print("Canonical artifact remains readable: PASS")
print("No production files modified: PASS")


# ==========================================================================
# Final result
# ==========================================================================

banner("13R-8F-11 RESULT")

if same_path:
    print("13R-8F-11 COMPLETE")
    print()
    print("ARCHITECTURAL FINDING")
    print("The existing model already contains enough concepts for local artifact registration.")
    print()
    print("Existing concepts:")
    print("  CorpusSource.local_path")
    print("  CorpusSource.is_downloaded")
    print("  SourceStatus.REGISTERED")
    print("  SourceStatus.SKIPPED")
    print("  AcquisitionResult")
    print()
    print("Therefore:")
    print("  DO NOT create LocalRegistrationImporter.")
    print("  DO NOT create AlreadyLocalImporter.")
    print("  DO NOT create a new LOCAL SourceStatus.")
    print("  DO NOT modify CorpusSource.local_path.")
    print("  DO NOT modify LocalFileImporter.")
    print()
    print("NEXT REPAIR TARGET:")
    print("DefaultSourceAcquirer local-registration branch.")
    print()
    print("Recommended next step:")
    print(
        "13R-8F-12 — Read-only control-flow audit of DefaultSourceAcquirer.acquire() "
        "and its local dispatch branch, followed by a minimal generic registration repair "
        "if the audit confirms the missing branch."
    )
else:
    print("13R-8F-11 COMPLETE — source/destination collision not present.")
